import os
import logging
from typing import List
import aiohttp
from datetime import datetime

from .models import (
    SOURCE_TYPES,
    WORK_TYPES,
    PUBLICATION_TYPES,
    Author,
    Entity,
    SearchInput,
    Work,
    Publication,
    Publisher,
    create_consistent_uuid,
)
from .http import ThrottledClientSession
from .user_agent import get_user_agent_header

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

async def search_google_books(search_input: SearchInput) -> List[Entity]:
    """
    Search for books using the Google Books API.

    Parameters:
    -----------
    search_input : SearchInput
        The search input containing the query and other search parameters.

    Returns:
    --------
    List[Entity]
        A list of Work entities representing the search results.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY environment variable is not set")
        return []

    params = {
        "q": search_input.query,
        "maxResults": search_input.num_results,
        "key": api_key
    }

    async with ThrottledClientSession(rate_limit=15/60, headers=get_user_agent_header()) as session:
        try:
            async with session.get(GOOGLE_BOOKS_API_URL, params=params) as response:
                if response.status == 403:
                    error_body = await response.text()
                    logger.error(f"403 Forbidden error in search_google_books. Response: {error_body}")
                    return []
                response.raise_for_status()
                data = await response.json()

                logger.info(f"API Response: {data}")  # Log the entire response

                if "items" not in data:
                    logger.warning(f"No items found in API response. Full response: {data}")
                    return []

                results: List[Entity] = []
                for item in data["items"]:
                    volume_info = item.get("volumeInfo", {})
                    work = Work(
                        id=create_consistent_uuid(item["id"]),
                        work_type=WORK_TYPES.BOOK,
                        name=volume_info.get("title", "Unknown Title"),
                        url=volume_info.get("infoLink", ""),
                        abstract=volume_info.get("description", ""),
                        source_type=SOURCE_TYPES.GOOGLE_BOOKS,
                        authors=[
                            Author(
                                id=create_consistent_uuid(author),
                                name=author,
                                source_type=SOURCE_TYPES.GOOGLE_BOOKS
                            ) for author in volume_info.get("authors", [])
                        ],
                        year=int(volume_info.get("publishedDate", "").split("-")[0]) if volume_info.get("publishedDate") else None,
                    )

                    if volume_info.get("publisher"):
                        publisher = Publisher(
                            id=create_consistent_uuid(volume_info["publisher"]),
                            name=volume_info["publisher"],
                            source_type=SOURCE_TYPES.GOOGLE_BOOKS
                        )
                        publication = Publication(
                            id=create_consistent_uuid(f"{volume_info['publisher']}_{work.id}"),
                            name=volume_info["publisher"],
                            source_type=SOURCE_TYPES.GOOGLE_BOOKS,
                            publication_type=PUBLICATION_TYPES.BOOK,
                            publisher=publisher
                        )
                        work.publications = [publication]

                    results.append(work)

                logger.info(f"Processed {len(results)} results")
                return results

        except aiohttp.ClientResponseError as e:
            logger.error(f"HTTP error {e.status} in search_google_books: {str(e)}")
            return []
        except aiohttp.ClientError as e:
            logger.error(f"Network error in search_google_books: {str(e)}")
            return []


async def download_from_google_books(work: Work) -> Work:
    """
    Download additional details for a book Work entity.

    Parameters:
    -----------
    work : Work
        The Work entity representing a book to download details for.

    Returns:
    --------
    Work
        The updated Work entity with additional details.
    """
    # Initialize full_text with a default value
    work.full_text = "No full text available"
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY environment variable is not set")
        return work  # Return the work with default full_text instead of raising an exception

    book_id = work.id
    url = f"{GOOGLE_BOOKS_API_URL}/{book_id}?key={api_key}"

    async with ThrottledClientSession(rate_limit=15/60, headers=get_user_agent_header()) as session:
        try:
            async with session.get(url) as response:
                if response.status == 403:
                    error_body = await response.text()
                    logger.error(f"403 Forbidden error in download_from_google_books for book {book_id}. Response: {error_body}")
                    return work
                response.raise_for_status()
                book_details = await response.json()

                logger.info(f"API Response for book {book_id}: {book_details}")  # Log the entire response

                volume_info = book_details.get('volumeInfo', {})

                work.abstract = volume_info.get('description', work.abstract or "No description available")
                work.full_text = volume_info.get('description', work.full_text)  # Use the default if not found

                work.authors = [
                    Author(
                        id=create_consistent_uuid(author),
                        name=author,
                        source_type=SOURCE_TYPES.GOOGLE_BOOKS
                    ) for author in volume_info.get('authors', [])
                ]

                published_date = volume_info.get('publishedDate')
                if published_date:
                    try:
                        work.year = datetime.strptime(published_date, "%Y-%m-%d").year
                    except ValueError:
                        try:
                            work.year = datetime.strptime(published_date, "%Y").year
                        except ValueError:
                            logger.warning(f"Could not parse published date: {published_date}")

                work.links = volume_info.get('categories', [])

                publisher_name = volume_info.get('publisher')
                if publisher_name:
                    publisher = Publisher(
                        id=create_consistent_uuid(publisher_name),
                        name=publisher_name,
                        source_type=SOURCE_TYPES.GOOGLE_BOOKS
                    )
                    publication = Publication(
                        id=create_consistent_uuid(f"{publisher_name}_{work.id}"),
                        name=publisher_name,
                        source_type=SOURCE_TYPES.GOOGLE_BOOKS,
                        publication_type=PUBLICATION_TYPES.BOOK,
                        publisher=publisher
                    )
                    work.publications = [publication]

                industry_identifiers = volume_info.get('industryIdentifiers', [])
                for identifier in industry_identifiers:
                    if identifier['type'] == 'ISBN_13':
                        work.doi = identifier['identifier']
                        break

                return work

        except aiohttp.ClientResponseError as e:
            logger.error(f"HTTP error {e.status} in download_from_google_books for book {book_id}: {str(e)}")
        except aiohttp.ClientError as e:
            logger.error(f"Network error in download_from_google_books for book {book_id}: {str(e)}")
        
        return work


async def search_and_download_from_google_books(search_input: SearchInput) -> List[Entity]:
    """
    Search for books and download additional details for each result.

    Parameters:
    -----------
    search_input : SearchInput
        The search input containing the query and other search parameters.

    Returns:
    --------
    List[Entity]
        A list of Work entities representing the search results with full details.
    """
    search_results = await search_google_books(search_input)
    downloaded_results: List[Entity] = []

    for result in search_results:
        if isinstance(result, Work):
            downloaded_work = await download_from_google_books(result)
            downloaded_results.append(downloaded_work)
        else:
            downloaded_results.append(result)

    return downloaded_results