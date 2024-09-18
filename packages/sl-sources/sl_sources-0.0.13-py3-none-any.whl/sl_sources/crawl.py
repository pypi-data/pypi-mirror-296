import asyncio
import hashlib
import json
import os
import re
import time
import traceback
from typing import Any, Dict, List, Optional, Union

import aiofiles
import aiohttp

from sl_sources.video import can_download_with_ytdlp

from .models import (
    ENTITY_MODELS,
    ENTITY_TYPES,
    SOURCE_TYPES,
    WORK_TYPES,
    Author,
    Entity,
    Institution,
    Publication,
    Publisher,
    SearchInput,
    Work,
)

from .http import cloud_function_request, resolve_url, validate_url
from .papers import get_paper_details
from .sources import download_search_result, search_and_download, search_source


class CacheManager:
    def __init__(self, cache_filename: str):
        self.cache_filename = cache_filename
        self.entities = {}
        self.searches = {}
        self.load_cache()
        self.lock = asyncio.Lock()

    def load_cache(self) -> None:
        if os.path.exists(self.cache_filename):
            with open(self.cache_filename, "r") as f:
                cache_data = json.load(f)
                self.entities = cache_data.get("entities", {})
                self.searches = cache_data.get("searches", {})

    async def update_cache(
        self,
        entity: Optional[Entity] = None,
        search_keyword: Optional[str] = None,
        search_results: Optional[List[Work]] = None,
    ) -> None:
        async with self.lock:
            if entity is not None:
                url_hash = self.get_entity_hash(entity)
                self.entities[url_hash] = (
                    entity.model_dump() if hasattr(entity, "model_dump") else entity
                )

            if search_keyword is not None and search_results is not None:
                self.searches[search_keyword] = [
                    result.model_dump() if hasattr(result, "model_dump") else result
                    for result in search_results
                ]

            await self.save_cache()

    async def save_cache(self) -> None:
        async with aiofiles.open(self.cache_filename, "w") as f:
            cache_data = {"entities": self.entities, "searches": self.searches}
            await f.write(json.dumps(cache_data, indent=2))
            print(f"**** Cache saved to {self.cache_filename}")

    def get_entity_hash(self, entity: Entity) -> str:
        return (
            hashlib.md5(entity.url.encode()).hexdigest()
            if hasattr(entity, "url")
            else entity.id
        )


async def crawl(
    keywords: List[str] = [],
    urls: List[str] = [],
    source_types: List[str] = [SOURCE_TYPES.OPENALEX, SOURCE_TYPES.GOOGLE_SCHOLAR],
    research_topic: str = "",
    max_concurrent_threads: int = 3,
    use_cloud_function: bool = False,
    entity_types: List[str] = [
        ENTITY_TYPES.WORK,
        ENTITY_TYPES.AUTHOR,
        ENTITY_TYPES.INSTITUTION,
        ENTITY_TYPES.PUBLICATION,
    ],
    num_results: int = 5,
    cache_filename: str = "manifest.json",
    max_depth: int = 3,
    rate_limit: float = 1.0,
) -> List[Entity]:
    print(f"Crawling with {len(keywords)} keywords and {len(urls)} URLs")

    # Validate and deduplicate URLs
    validated_urls: List[str] = []
    for url in urls:
        try:
            validated_url = validate_url(url)
            validated_urls.append(validated_url)
        except ValueError as e:
            print(f"Skipping invalid URL: {url}. Error: {str(e)}")
            continue

    urls: set = set(validated_urls)
    keywords: set = set(keywords)

    # Normalize and categorize URLs
    arxiv_urls: List[str] = [url for url in urls if "arxiv.org/" in url]
    biorxiv_urls: List[str] = [url for url in urls if "biorxiv.org/" in url]
    pubmed_urls: List[str] = [url for url in urls if "pubmed.ncbi.nlm.nih.gov/" in url]
    media_urls: List[str] = [url for url in urls if can_download_with_ytdlp(url)]
    doi_urls: List[str] = [url for url in urls if "doi.org/" in url]

    # Remove categorized URLs from the main list
    urls = [
        url
        for url in urls
        if "arxiv.org" not in url
        and "biorxiv.org" not in url
        and "pubmed.ncbi.nlm.nih.gov/" not in url
        and "doi.org/" not in url
        and not can_download_with_ytdlp(url)
    ]

    url_sources: List[Work] = []

    # Create Work objects for each type of URL
    for url in doi_urls:
        id: str = url.split("doi.org/")[1]
        url_sources.append(
            Work(
                id=id,
                name=f"DOI: {id}",
                url=f"https://doi.org/{id}",
                source_type=SOURCE_TYPES.DOI,
                work_type=WORK_TYPES.PAPER,
            )
        )
    for url in arxiv_urls:
        id: str = url.split("/")[-1]
        url_sources.append(
            Work(
                id=id,
                name=f"arXiv: {id}",
                url=url,
                source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                work_type=WORK_TYPES.PAPER,
            )
        )
    for url in biorxiv_urls:
        id: str = re.search(r"(?:biorxiv\.org/content/)(.+)", url).group(1)
        url_sources.append(
            Work(
                id=id,
                name=f"bioRxiv: {id}",
                url=url,
                source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                work_type=WORK_TYPES.PAPER,
            )
        )
    for url in pubmed_urls:
        id: str = url.split("/")[-1]
        url_sources.append(
            Work(
                id=id,
                name=f"PubMed: {id}",
                url=url,
                source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                work_type=WORK_TYPES.PAPER,
            )
        )
    for url in media_urls:
        source_type = SOURCE_TYPES.VIDEO
        id = url
        if "youtube" in id:
            id = id.split("v=")[-1].split("&")[0]
        elif "vimeo" in id:
            id = id.split("/")[-1].split("?")[0]
        elif "dailymotion" in id:
            id = id.split("/")[-1].split("?")[0]

        url_sources.append(
            Work(
                id=id,
                name=f"Media: {id}",
                url=url,
                source_type=source_type,
                work_type=WORK_TYPES.VIDEO,
            )
        )

    # Create a cache manager instance
    cache_manager = CacheManager(cache_filename)

    # Create queues for search and download tasks
    search_queue = asyncio.Queue()
    download_queue = asyncio.Queue()

    # Create semaphores for search and download operations
    search_semaphore = asyncio.Semaphore(max_concurrent_threads)
    download_semaphore = asyncio.Semaphore(max_concurrent_threads)

    # Create a list to store the results
    results: List[Entity] = []

    # Create search worker tasks
    search_workers = [
        asyncio.create_task(
            search_worker(
                search_queue,
                download_queue,
                search_semaphore,
                use_cloud_function,
                rate_limit,
                cache_manager,
            )
        )
        for _ in range(max_concurrent_threads)
    ]

    # Create download worker tasks
    download_workers = [
        asyncio.create_task(
            download_worker(
                download_queue,
                download_semaphore,
                use_cloud_function,
                research_topic,
                entity_types,
                cache_manager,
                results,
                max_depth,
                rate_limit,
            )
        )
        for _ in range(max_concurrent_threads)
    ]

    # Add initial search tasks to the queue
    for source_type in source_types:
        for keyword in keywords:
            if keyword in cache_manager.searches:
                # Use cached search results if available
                cached_results = cache_manager.searches[keyword]
                for result in cached_results:
                    await download_queue.put(result)
            else:
                # Add search task to the queue
                await search_queue.put(
                    SearchInput(
                        entity_types=entity_types,
                        query=keyword,
                        num_results=num_results,
                        source_type=source_type,
                    )
                )

    # Add initial URL sources to the download queue
    for source in url_sources:
        await download_queue.put(source)

    # Wait for all search tasks to complete
    await search_queue.join()

    # Wait for all download tasks to complete
    await download_queue.join()

    # Cancel worker tasks
    for worker in search_workers + download_workers:
        worker.cancel()

    # Wait for all worker tasks to be cancelled
    await asyncio.gather(*search_workers, *download_workers, return_exceptions=True)

    print(
        f"Crawl completed. Check the 'downloaded_data' directory {cache_filename} and for results."
    )

    # Return the results
    return results


async def search_worker(
    search_queue,
    download_queue,
    semaphore,
    use_cloud_function,
    rate_limit,
    cache_manager,
):
    while True:
        search_input = await search_queue.get()
        try:
            async with semaphore:
                if search_input.query in cache_manager.searches:
                    # Use cached search results if available
                    cached_results = cache_manager.searches[search_input.query]
                    for result in cached_results:
                        await download_queue.put(result)
                else:
                    # Perform a new search
                    results = await _search_and_add_to_queue(
                        search_input, use_cloud_function
                    )
                    for result in results:
                        await download_queue.put(result)
                    # Update the cache with the new search results
                    await cache_manager.update_cache(
                        search_keyword=search_input.query, search_results=results
                    )
        except Exception as e:
            print(f"Error in search worker: {e}")
        finally:
            search_queue.task_done()
        await asyncio.sleep(rate_limit)


async def download_worker(
    download_queue,
    semaphore,
    use_cloud_function,
    research_topic,
    entity_types,
    cache_manager,
    results,
    max_depth,
    rate_limit,
):
    while True:
        item = await download_queue.get()
        try:
            if isinstance(item, dict):
                item = Work(**item)

            result = None
            async with semaphore:
                result = await _download_and_evaluate(
                    item,
                    0,
                    max_depth,
                    use_cloud_function,
                    research_topic,
                    entity_types,
                    cache_manager,
                )

            if result is not None:
                results.append(result)
                await cache_manager.update_cache(entity=result)

                if result.relevant:
                    await _crawl_links(
                        result.links,
                        depth=1,
                        max_depth=max_depth,
                        cache_manager=cache_manager,
                        parent_source=item,
                        use_cloud_function=use_cloud_function,
                        research_topic=research_topic,
                        entity_types=entity_types,
                    )
        except Exception as e:
            print(f"Error in download worker: {e}")
            traceback.print_exc()
        finally:
            download_queue.task_done()
        await asyncio.sleep(rate_limit)


async def _search_and_add_to_queue(
    search_input: SearchInput, use_cloud_function: bool
) -> List[Work]:
    if use_cloud_function:
        results = await cloud_function_request(
            "search_and_download",
            {
                "source_types": [search_input.source_type],
                "query": search_input.query,
                "num_results": search_input.num_results,
                "entity_types": search_input.entity_types,
            },
        )
    else:
        results = await search_source(search_input)

    return results


async def _download_and_evaluate(
    source: Work,
    depth: int,
    max_depth: int,
    use_cloud_function: bool,
    research_topic: str,
    entity_types: List[str],
    cache_manager: CacheManager,
) -> Entity:
    url: str = source.url
    print(f"Starting download_and_evaluate for {url}")

    try:
        url = validate_url(url)
        if "semanticscholar.org" in url:
            source.source_type = SOURCE_TYPES.SEMANTIC_SCHOLAR
    except ValueError as e:
        print(f"Skipping invalid URL: {url}. Error: {str(e)}")
        return source

    url_hash: str = cache_manager.get_entity_hash(source)

    if url_hash in cache_manager.entities:
        print(f"Using cached content for {url}")
        cached_entity = cache_manager.entities[url_hash]
        if isinstance(cached_entity, dict):
            return Work(**cached_entity)
        return cached_entity

    print(f"Downloading {url}")
    if use_cloud_function:
        entity_data = await cloud_function_request(
            "download_search_result",
            {"search_result": source.model_dump_json()},
        )
        type = entity_data.get("type")
        entity = ENTITY_MODELS[type](**entity_data)
    else:
        print("Downloading search result")
        entity = await download_search_result(source)

    if not entity:
        print(f"No content downloaded for {url}")
        entity = Work(
            id=url_hash,
            url=url,
            name=f"No content: {url}",
            abstract="No content downloaded",
            source_type=SOURCE_TYPES.CRAWL,
            work_type=WORK_TYPES.UNKNOWN,
        )
        await cache_manager.update_cache(entity=entity)
        return entity

    text = entity.full_text if entity.full_text else ""
    print(f"Downloaded content for {url}: {str(text)[:100]}...")

    print(f"Evaluating page for {url}")
    result: Dict[str, Any] = await _evaluate_page(text, research_topic)
    print(f"Evaluation result for {url}: {result}")

    if isinstance(entity, Work) and entity.type == ENTITY_TYPES.WORK:
        entity.abstract = result["abstract"]
        entity.relevant = result["relevant"]
        entity.full_text = text
        entity.links = result["links"]

    await cache_manager.update_cache(entity=entity)
    print(f"Added to cache: {url}")

    return entity


def read_cache(cache_filename: str) -> Dict[str, Any]:
    """
    Read the cache from a JSON file.
    """
    # Load or create cache
    cache: Dict[str, Any] = {}
    if os.path.exists(cache_filename):
        with open(cache_filename, "r") as f:
            cache = json.load(f)
    return cache


async def process_url(
    url: str,
    use_cloud_function: bool,
    research_topic: str,
    entity_types: List[str],
    cache: Dict[str, Any],
    cache_filename: str,
    max_depth: int,
    depth: int = 0,
) -> Optional[Entity]:
    print(f"Processing URL: {url}")

    try:
        # Validate the URL
        url = validate_url(url)
        source_type = SOURCE_TYPES.CRAWL
        if "semanticscholar.org" in url:
            source_type = SOURCE_TYPES.SEMANTIC_SCHOLAR
    except ValueError as e:
        print(f"Skipping invalid URL: {url}. Error: {str(e)}")
        return None

    # Generate a unique hash for the URL
    url_hash: str = hashlib.md5(url.encode()).hexdigest()

    # Check if the URL is already in the cache
    if url_hash in cache:
        print(f"Using cached content for {url}")
        cached_entity = cache[url_hash]
        if isinstance(cached_entity, dict):
            # Convert dict to Work entity if necessary
            return Work(**cached_entity)
        return cached_entity

    try:
        print(f"Downloading {url}")
        if use_cloud_function:
            # Use cloud function to download content
            entity_data = await cloud_function_request(
                "download_search_result",
                {
                    "search_result": Work(
                        url=url, source_type=source_type
                    ).model_dump_json()
                },
            )
            type = entity_data.get("type")
            entity = ENTITY_MODELS[type](**entity_data)
        else:
            # Download search result locally
            entity = await download_search_result(
                Work(url=url, source_type=source_type)
            )

        if not entity:
            print(f"No content downloaded for {url}")
            # Create a placeholder Work entity if no content was downloaded
            entity = Work(
                id=url_hash,
                url=url,
                name=f"No content: {url}",
                abstract="No content downloaded",
                source_type=source_type,
                work_type=WORK_TYPES.UNKNOWN,
            )
            # Update the cache with the placeholder entity
            await update_cache(cache, entity, cache_filename)
            return entity

        # Extract full text
        text = entity.full_text if entity.full_text else ""

        print(f"Downloaded content for {url}: {str(text)[:100]}...")

        print(f"Evaluating page for {url}")
        # Evaluate the page content for relevance
        result: Dict[str, Any] = await _evaluate_page(text, research_topic)
        print(f"Evaluation result for {url}: {result}")

        # Update the entity with evaluation results
        if isinstance(entity, Work) and entity.type == ENTITY_TYPES.WORK:
            entity.abstract = result["abstract"]
            entity.relevant = result["relevant"]
            entity.full_text = text
            entity.links = result["links"]

        # Update the cache with the new entity
        await update_cache(cache, entity, cache_filename)
        print(f"Added to cache: {url}")

        if result["relevant"] and depth < max_depth:
            # If the content is relevant and we haven't reached max depth, crawl the links found in the page
            for link in result["links"]:
                await process_url(
                    link,
                    use_cloud_function,
                    research_topic,
                    entity_types,
                    cache,
                    cache_filename,
                    max_depth,
                    depth + 1,
                )

        return entity

    except Exception as e:
        print(f"Error processing {url}: {e}")
        print(traceback.format_exc())
        # Create an error Work entity if an exception occurs
        error_entity = Work(
            id=url_hash,
            url=url,
            name=f"Error: {url}",
            abstract=str(e),
            source_type=source_type,
            work_type=WORK_TYPES.UNKNOWN,
        )
        # Update the cache with the error entity
        await update_cache(cache, error_entity, cache_filename)
        return error_entity


# Helper functions


def read_cache(cache_filename: str) -> Dict[str, Any]:
    """
    Read the cache from a JSON file.
    """
    import json
    import os

    cache: Dict[str, Any] = {}
    if os.path.exists(cache_filename):
        with open(cache_filename, "r") as f:
            cache = json.load(f)
    return cache


async def update_cache(
    cache: Dict[str, Any],
    entity: Optional[Entity] = None,
    search_keyword: Optional[str] = None,
    search_results: Optional[List[Work]] = None,
    filename: str = "manifest.json",
) -> None:
    async with aiofiles.open(filename, "r") as f:
        cache_data = json.loads(await f.read())

    if entity is not None:
        url_hash = (
            hashlib.md5(entity.url.encode()).hexdigest()
            if hasattr(entity, "url")
            else entity.id
        )
        cache_data["entities"][url_hash] = (
            entity.model_dump() if hasattr(entity, "model_dump") else entity
        )

    if search_keyword is not None and search_results is not None:
        cache_data["searches"][search_keyword] = [
            result.model_dump() if hasattr(result, "model_dump") else result
            for result in search_results
        ]

    async with aiofiles.open(filename, "w") as f:
        await f.write(json.dumps(cache_data, indent=2))
        print(f"Cache written to {filename}")


async def _evaluate_page(
    text: str, research_topic: str, model: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    OPENAI_API_KEY: Optional[str] = os.getenv(
        "OPENAI_API_KEY", os.getenv("SOCIETY_API_KEY")
    )
    if not OPENAI_API_KEY:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    # Truncate the text if it's too long
    max_length: int = 128000
    if len(text) > max_length:
        text = text[:max_length] + "..."

    # Construct the prompt for the OpenAI API
    prompt: str = f"""
    Analyze the following text and determine if it's relevant. 
    Also extract any URLs mentioned in the text that seem relevant to these topics.
    
    Text:
    {text}
    
    We are researching the following topic and related domains:
    {research_topic}

    Please evaluate if the text above contains relevant and substantive information for our research.

    Respond with a JSON object containing two fields:
    1. "relevant": a boolean indicating if the text is relevant
    2. "links": a list of relevant URLs extracted from the text which are worth looking at. Ignore links that are not relevant to the research topic.
    3. "abstract": a summary of the text, focusing on the most relevant information for the research topic.
    
    Example response:
    {{
        "relevant": true,
        "links": ["https://example.com/ai-article", "https://example.org/ml-study"],
        "abstract": "A summary of the text, focusing on the most relevant information for the research topic."
    }}
    """

    # Make a request to the OpenAI API
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            },
        ) as response:
            if response.status == 200:
                result: Dict[str, Any] = await response.json()
                try:
                    # Parse the API response
                    evaluation: str = result["choices"][0]["message"]["content"]
                    evaluation = evaluation.replace("```json\n", "").replace(
                        "\n```", ""
                    )
                    evaluation_dict: Dict[str, Any] = json.loads(evaluation)
                    evaluation_dict["text"] = text
                    return evaluation_dict
                except json.JSONDecodeError:
                    print(
                        f"Error parsing GPT-4 response: {result['choices'][0]['message']['content']}"
                    )
                    return {
                        "relevant": False,
                        "links": [],
                        "abstract": "",
                        "text": text,
                    }
            else:
                print(f"Error calling OpenAI API: {response.status}")
                return {"relevant": False, "links": [], "abstract": "", "text": text}


async def _crawl_links(
    links: List[str],
    depth: int,
    max_depth: int,
    cache_manager: CacheManager,
    parent_source: Optional[Union[Work, Dict[str, Any]]] = None,
    use_cloud_function: bool = False,
    research_topic: Optional[str] = None,
    entity_types: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    print(f"Crawling links at depth {depth}")
    if depth > max_depth:
        return []

    source_type: str = (
        parent_source.source_type
        if isinstance(parent_source, Work)
        else SOURCE_TYPES.CRAWL
    )

    tasks: List[asyncio.Task] = []
    for link in links:
        try:
            if isinstance(parent_source, Work):
                resolved_url: str = resolve_url(link, base_url=parent_source.url)
            elif isinstance(parent_source, dict) and "url" in parent_source:
                resolved_url: str = resolve_url(link, base_url=parent_source["url"])
            else:
                resolved_url: str = resolve_url(link)
        except ValueError as e:
            print(f"Skipping invalid URL: {link}. Error: {str(e)}")
            url_hash: str = cache_manager.get_entity_hash(
                Work(url=link, source_type=source_type, name=f"Invalid URL: {link}")
            )
            error_entity = Work(
                id=url_hash,
                url=link,
                name="Invalid URL",
                abstract=str(e),
                source_type=source_type,
                work_type=WORK_TYPES.UNKNOWN,
                authors=[],
                relevant=False,
            )
            await cache_manager.update_cache(entity=error_entity)
            continue

        url_hash: str = cache_manager.get_entity_hash(
            Work(
                url=resolved_url,
                source_type=source_type,
                name=f"Crawled URL: {resolved_url}",
            )
        )

        if url_hash in cache_manager.entities:
            print(f"URL {resolved_url} already processed or in cache")
            continue

        task: asyncio.Task = asyncio.create_task(
            _process_link(
                resolved_url,
                depth,
                max_depth,
                source_type=source_type,
                parent_source=parent_source,
                use_cloud_function=use_cloud_function,
                research_topic=research_topic,
                entity_types=entity_types,
                cache_manager=cache_manager,
            )
        )
        tasks.append(task)

    results: List[Optional[Dict[str, Any]]] = await asyncio.gather(
        *tasks, return_exceptions=True
    )
    return [
        result
        for result in results
        if result is not None and not isinstance(result, Exception)
    ]


async def _process_link(
    url: str,
    depth: int,
    max_depth: int,
    source_type: str,
    parent_source: Optional[Dict[str, Any]],
    use_cloud_function: bool,
    research_topic: str,
    entity_types: List[str],
    cache_manager: CacheManager,
) -> Optional[Work]:
    print(f"Processing link: {url}")

    try:
        work: Work = await get_paper_details(url)
        if work is None:
            abstract = f"Crawled from {url}"
            name = "Unknown crawled link"
            if parent_source is not None:
                if isinstance(parent_source, dict):
                    abstract = f"Crawled from {url} with parent {parent_source['name']} | {parent_source['url']}"
                    name = parent_source["name"]
                else:
                    abstract = f"Crawled from {url} with parent {parent_source.name} | {parent_source.url}"
                    name = parent_source.name

            work = Work(
                id=hashlib.md5(url.encode()).hexdigest(),
                work_type=WORK_TYPES.UNKNOWN,
                name=name,
                authors=[],
                abstract=abstract,
                url=url,
                source_type=source_type,
            )

        if work:
            print(f"Work found: {work}")
            result: Entity = await _download_and_evaluate(
                work,
                depth + 1,
                max_depth,
                use_cloud_function,
                research_topic,
                entity_types,
                cache_manager,
            )
            return result
        else:
            print(f"No work found for {url}")
            return None
    except Exception as e:
        print(f"Error processing link {url}: {e}")
        traceback.print_exc()
        return None
