import asyncio
import hashlib
import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from dotenv import load_dotenv
import aiohttp
from aiolimiter import AsyncLimiter

from .models import SOURCE_TYPES, Work, SearchInput, Entity
from .scrape import browser_scrape

# Load environment variables from .env file
load_dotenv()

# Configuration
class Config:
    GOOGLE_SEARCH_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_RATE_LIMIT: int = 10  # requests per second
    OPENAI_RATE_LIMIT: int = 60  # requests per minute
    MAX_RETRIES: int = 3
    CACHE_EXPIRY: int = 3600  # 1 hour in seconds
    MAX_CACHE_SIZE: int = 1000  # Maximum number of items in cache

config = Config()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiters
google_limiter = AsyncLimiter(config.GOOGLE_RATE_LIMIT, 1)
openai_limiter = AsyncLimiter(config.OPENAI_RATE_LIMIT, 60)

# Simple cache with size limit
cache: Dict[str, Dict[str, Any]] = {}

def add_to_cache(key: str, value: Any) -> None:
    if len(cache) >= config.MAX_CACHE_SIZE:
        oldest_key = min(cache, key=lambda k: cache[k]['timestamp'])
        del cache[oldest_key]
    cache[key] = {'data': value, 'timestamp': datetime.now()}

async def extract_work_info(title: str, url: str, abstract: str, full_text: str) -> Dict[str, List[str]]:
    """
    Use GPT-4o-mini to extract authors, institutions, and publications from the work's information.
    """
    cache_key = hashlib.md5(f"{title}{url}{abstract}".encode()).hexdigest()
    if cache_key in cache and datetime.now() - cache[cache_key]['timestamp'] < timedelta(seconds=config.CACHE_EXPIRY):
        return cache[cache_key]['data']

    prompt = f"""
    Given the following information about a work, please extract the authors, institutions, and publications.
    If any of these cannot be determined, return an empty list for that field.

    Title: {title}
    URL: {url}
    Abstract: {abstract}
    Full Text: {full_text[:1000]}  # Truncated for brevity

    Please return the information in the following JSON format:
    {{
        "authors": ["Author 1", "Author 2", ...],
        "institutions": ["Institution 1", "Institution 2", ...],
        "publications": ["Publication 1", "Publication 2", ...]
    }}
    """

    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "functions": [{
            "name": "extract_work_info",
            "description": "Extract authors, institutions, and publications from work information",
            "parameters": {
                "type": "object",
                "properties": {
                    "authors": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of authors"
                    },
                    "institutions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of institutions"
                    },
                    "publications": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of publications"
                    }
                },
                "required": ["authors", "institutions", "publications"]
            }
        }],
        "function_call": {"name": "extract_work_info"}
    }

    async with openai_limiter:
        async with aiohttp.ClientSession() as session:
            for attempt in range(config.MAX_RETRIES):
                try:
                    async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data) as response:
                        response_json = await response.json()
                        if response.status != 200:
                            raise aiohttp.ClientResponseError(response.request_info, response.history, status=response.status, message=f"API request failed: {response_json}")
                        
                        function_call = response_json['choices'][0]['message']['function_call']
                        result = json.loads(function_call['arguments'])
                        add_to_cache(cache_key, result)
                        return result
                except aiohttp.ClientResponseError as e:
                    logger.error(f"API request failed: {e}")
                    if attempt == config.MAX_RETRIES - 1:
                        raise
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON: {e}")
                    if attempt == config.MAX_RETRIES - 1:
                        return {"authors": [], "institutions": [], "publications": []}
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
                    if attempt == config.MAX_RETRIES - 1:
                        raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

async def search_google(search_input: SearchInput) -> List[Work]:
    """
    Perform a Google search using the Custom Search JSON API.
    """
    results: List[Work] = []
    google_api_url: str = "https://customsearch.googleapis.com/customsearch/v1"

    params: Dict[str, Any] = {
        "key": config.GOOGLE_SEARCH_API_KEY,
        "cx": config.CSE_ID,
        "q": search_input.query,
        "num": search_input.num_results,
    }

    if search_input.file_type:
        params["fileType"] = search_input.file_type

    async with google_limiter:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(google_api_url, params=params) as response:
                    if response.status != 200:
                        raise aiohttp.ClientResponseError(response.request_info, response.history, status=response.status, message=f"Google API request failed with status {response.status}")
                    response_json: Dict[str, Any] = await response.json()

                if "items" in response_json:
                    for item in response_json["items"]:
                        url: str = item.get("link", "")
                        id: str = hashlib.md5(url.encode()).hexdigest()
                        work = Work(
                            id=id,
                            name=item.get("title", ""),
                            url=url,
                            abstract=item.get("snippet", ""),
                            full_text="",
                            authors=[],
                            institutions=[],
                            publications=[],
                            source_type=SOURCE_TYPES.GOOGLE,
                        )
                        results.append(work)
            except aiohttp.ClientResponseError as e:
                logger.error(f"Google API request failed: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in Google search: {e}")
                raise

    return results

async def download_from_google_search(work: Work) -> Work:
    """
    Download and extract the full text content for a given Work object.
    Also extract additional information using GPT-4o-mini.
    """
    try:
        work.full_text = await browser_scrape(work.url)
        extracted_info = await extract_work_info(work.name, work.url, work.abstract, work.full_text)
        work.authors = extracted_info["authors"]
        work.institutions = extracted_info["institutions"]
        work.publications = extracted_info["publications"]
        return work
    except Exception as e:
        logger.error(f"Error processing {work.url}: {e}")
        return work

async def search_and_download_from_google(search_input: SearchInput) -> List[Entity]:
    """
    Perform a Google search and download full text content for the results.
    """
    search_results: List[Work] = await search_google(search_input)
    tasks = [download_from_google_search(result) for result in search_results]
    entities: List[Entity] = await asyncio.gather(*tasks)
    return entities