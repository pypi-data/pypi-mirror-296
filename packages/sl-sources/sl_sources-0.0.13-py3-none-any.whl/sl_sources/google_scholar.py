import asyncio
import io
import logging
import re
import traceback
from typing import List, Optional, Tuple

import aiohttp
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright
from pypdf import PdfReader

from .google import search_google
from .http import ThrottledClientSession
from .models import (ENTITY_TYPES, INSTITUTION_TYPES, PUBLICATION_TYPES,
                     SOURCE_TYPES, WORK_TYPES, Author, Entity, Institution,
                     Publication, Publisher, SearchInput, Work,
                     create_consistent_uuid)
from .scrape import browser_scrape, get_browser_and_page
from .user_agent import get_user_agent_header

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def search_and_download_from_google_scholar(
    search_input: SearchInput,
) -> List[Entity]:
    """
    Search Google Scholar and download full text content for the search results.

    This function performs a search on Google Scholar, processes the results,
    and attempts to download the full text for each work found.

    Parameters
    ----------
    search_input : SearchInput
        An object containing search parameters such as query, number of results,
        and entity types to search for.

    Returns
    -------
    List[Entity]
        A list of Entity objects (Works, Authors, Publications) found and processed.

    Notes
    -----
    This function uses a rate-limited client session to respect Google Scholar's
    usage policies. It also handles deduplication of publications.
    """
    logging.info(f"Starting search with input: {search_input}")

    # Perform the initial search on Google Scholar
    search_results = await search_google_scholar(search_input)

    entities: List[Entity] = []
    publications_set = set()  # To keep track of unique publications

    # Create a rate-limited client session for downloading content
    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        for result in search_results:
            if isinstance(result, Work):
                # Process Work entities
                entities.append(result)
                # Add authors to the entities list
                for author in result.authors:
                    if author not in entities:
                        entities.append(author)
                # Add publications to the entities list, avoiding duplicates
                for publication in result.publications:
                    if publication.id not in publications_set:
                        entities.append(publication)
                        publications_set.add(publication.id)

                try:
                    # Attempt to download the full text for the work
                    result = await download_from_google_scholar(result, session)
                    entities.append(result)
                except Exception as e:
                    logging.error(f"Error downloading full text for {result.name}: {e}")
                    entities.append(result)
            elif isinstance(result, Author):
                # Process Author entities
                entities.append(result)
            elif isinstance(result, Publication):
                # Process Publication entities, avoiding duplicates
                if result.id not in publications_set:
                    entities.append(result)
                    publications_set.add(result.id)

    logging.info(f"Total entities found: {len(entities)}")
    return entities


async def search_google_scholar(search_input: SearchInput) -> List[Entity]:
    query: str = search_input.query
    num_results: int = search_input.num_results
    entity_types: List[str] = search_input.entity_types

    results: List[Entity] = []
    seen_authors = set()
    seen_institutions = set()

    async with async_playwright() as p:
        try:
            browser, page = await get_browser_and_page(p)
            search_url: str = (
                f"https://scholar.google.com/scholar?q={query}&num={num_results}"
            )
            logging.info(f"Navigating to: {search_url}")

            await page.goto(search_url, wait_until="networkidle", timeout=60000)
            await asyncio.sleep(3)

            if await page.query_selector("#captcha-form"):
                logging.error("CAPTCHA detected. Google is blocking our requests.")
                return results

            items = await page.query_selector_all("#gs_res_ccl_mid > div")
            logging.info(f"Found {len(items)} items on the page")

            for item in items:
                try:
                    title_element = await item.query_selector("h3 a")
                    name: str = (
                        await title_element.inner_text() if title_element else ""
                    )
                    url: str = (
                        await title_element.get_attribute("href")
                        if title_element
                        else ""
                    )

                    authors_year_element = await item.query_selector(".gs_a")
                    authors_year_text: str = (
                        await authors_year_element.inner_text()
                        if authors_year_element
                        else ""
                    )
                    authors, publication, year, institutions = (
                        _parse_authors_year_institutions(authors_year_text)
                    )

                    snippet_element = await item.query_selector(".gs_rs")
                    snippet: str = (
                        await snippet_element.inner_text() if snippet_element else ""
                    )

                    doi = await _extract_doi(page, url)

                    logging.info(
                        f"Extracted data: Title: {name}, Authors: {authors}, Year: {year}, "
                        f"Publication: {publication}, Institutions: {institutions}, DOI: {doi}"
                    )

                    # Create a Work entity
                    work = Work(
                        work_type=WORK_TYPES.PAPER,
                        id=create_consistent_uuid(name),
                        source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                        name=name,
                        url=url,
                        abstract=snippet,
                        full_text="",
                        year=year,
                        doi=doi,
                        authors=[],
                        institutions=[],
                    )

                    for author, author_institutions in zip(authors, institutions):
                        author_id = create_consistent_uuid(author)
                        author_entity = Author(
                            id=author_id,
                            name=author,
                            source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                            institutions=[],
                        )

                        for inst in author_institutions:
                            inst_id = create_consistent_uuid(inst)
                            institution_entity = Institution(
                                id=inst_id,
                                name=inst,
                                source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                                institution_type=INSTITUTION_TYPES.ACADEMIC,
                            )
                            author_entity.institutions.append(institution_entity)
                            if inst_id not in seen_institutions:
                                seen_institutions.add(inst_id)
                                if "institution" in entity_types:
                                    results.append(institution_entity)

                        work.authors.append(author_entity)
                        if author_id not in seen_authors:
                            seen_authors.add(author_id)
                            if "author" in entity_types:
                                results.append(author_entity)

                    if publication:
                        publisher = _extract_publisher(publication)
                        pub = Publication(
                            id=create_consistent_uuid(publication),
                            name=publication,
                            source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                            publication_type=PUBLICATION_TYPES.JOURNAL,
                            publisher=publisher,
                        )
                        work.publications.append(pub)
                        if "publication" in entity_types:
                            results.append(pub)

                    # Update the institutions attribute of the Work object
                    work.institutions = list(seen_institutions)
                    results.append(work)

                except Exception as e:
                    logging.error(f"Error processing item: {e}")
                    logging.error(f"Item HTML: {await item.inner_html()}")

        except PlaywrightTimeoutError:
            logging.error("Timeout while loading Google Scholar page")
        except Exception as e:
            logging.error(f"Unexpected error during Google Scholar search: {e}")
            logging.error(f"Traceback: {traceback.format_exc()}")
        finally:
            await browser.close()

    logging.info(f"Total results found: {len(results)}")
    return results[:num_results]


def _parse_authors_year_institutions(
    authors_year_text: str,
) -> Tuple[List[str], str, Optional[int], List[List[str]]]:
    import re

    year_match = re.search(r"\b(19|20)\d{2}\b", authors_year_text)
    if year_match:
        year = int(year_match.group())
        authors_publication = authors_year_text.replace(str(year), "").strip()
    else:
        year = None
        authors_publication = authors_year_text.strip()

    parts = authors_publication.split(" - ", 1)
    authors_part = parts[0].strip()
    publication = parts[1].strip() if len(parts) > 1 else ""

    institution_keywords = (
        r"University|Institute|College|School|Center|Laboratory|Academy|Foundation"
    )
    author_list = re.split(r",\s*(?=[^,]+(?:,\s*[^,]+)*$)", authors_part)

    authors = []
    institutions = []

    for author in author_list:
        author = author.strip()
        author_parts = author.split(", ")
        author_name = author_parts[0]
        authors.append(author_name)

        if len(author_parts) > 1:
            institution_match = re.search(
                rf"({institution_keywords}.*?)(?=$)", author_parts[1]
            )
            if institution_match:
                institutions.append([institution_match.group(1).strip()])
            else:
                institutions.append([])
        else:
            institutions.append([])

    return authors, publication, year, institutions


def _extract_publisher(publication: str) -> Optional[Publisher]:
    known_publishers = [
        "Elsevier",
        "Springer",
        "Wiley",
        "IEEE",
        "Taylor & Francis",
        "SAGE",
        "Oxford University Press",
        "Cambridge University Press",
        "Nature Publishing Group",
        "ACM",
        "ACS",
        "AIP",
        "APS",
        "ASME",
        "IOP",
        "MDPI",
        "PLOS",
        "RSC",
        "SPIE",
    ]

    try:
        for publisher_name in known_publishers:
            if publisher_name.lower() in publication.lower():
                return Publisher(
                    id=create_consistent_uuid(publisher_name),
                    name=publisher_name,
                    source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                )
    except Exception as e:
        logging.error(f"Error extracting publisher: {e}")

    return None


async def _extract_doi(page, url: str) -> Optional[str]:
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=10000)
        doi_element = await page.query_selector('meta[name="citation_doi"]')
        if doi_element:
            return await doi_element.get_attribute("content")

        content = await page.content()
        doi_match = re.search(r"\b(10\.\d{4,}(?:\.\d+)*\/\S+)\b", content)
        if doi_match:
            return doi_match.group(1)
    except Exception as e:
        logging.error(f"Error extracting DOI: {e}")

    return None


async def download_from_google_scholar(
    work: Work, session: ThrottledClientSession
) -> Work:
    """
    Download the full text content for a given work from Google Scholar.

    This function attempts to download the full text of a work using various methods,
    including direct download, Google search for PDFs, and web scraping.

    Parameters
    ----------
    work : Work
        The Work object containing information about the publication to download.
    session : ThrottledClientSession
        A rate-limited aiohttp client session for making HTTP requests.

    Returns
    -------
    Work
        The Work object with the full text content if successfully downloaded, or the original Work object if not.

    Notes
    -----
    This function tries multiple approaches to obtain the full text:
    1. Direct download from the work's URL
    2. Google search for a PDF of the work
    3. Web scraping of the work's URL
    """
    if work.type != ENTITY_TYPES.WORK:
        raise ValueError("Work is required to download full text")
    if not work.url:
        raise ValueError("Work URL is required to download full text")

    try:
        # Attempt to download and extract text from the primary URL
        full_text = await _download_and_extract_text(work.url, session)
        work.full_text = full_text
        return work
    except aiohttp.ClientResponseError as e:
        logging.error(
            f"Could not get the full text from the primary URL: {work.url}\nContinuing with other approaches..."
        )

    # If primary URL fails, search Google for a PDF
    search_results = await search_google(
        SearchInput(
            query=f'"{work.name}"',
            file_type="pdf",
            num_results=3,
            source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
            entity_types=[ENTITY_TYPES.WORK],
        )
    )
    for search_result in search_results:
        try:
            # Attempt to download and extract text from each search result
            text = await _download_and_extract_text(search_result.url, session)
            if text:
                work.url = search_result.url
                work.full_text = text
                return work
        except Exception as e:
            logging.error(f"Error downloading PDF from Google search: {e}")

    try:
        # If all else fails, attempt to scrape the text from the webpage
        text = await browser_scrape(work.url)
        if text:
            work.url = work.url
            work.full_text = text
            return work
    except Exception as e:
        logging.error(f"Error scraping full text: {e}")

    # If no method succeeds, return an empty string
    raise ValueError("Could not download full text")


async def _download_and_extract_text(url: str, session: aiohttp.ClientSession) -> str:
    """
    Download content from a URL and extract text, handling both PDFs and web pages.

    This function attempts to download content from a given URL and extract
    text from it. It can handle both PDF files and regular web pages.

    Parameters
    ----------
    url : str
        The URL to download content from.
    session : aiohttp.ClientSession
        An aiohttp client session for making HTTP requests.

    Returns
    -------
    str
        The extracted text content from the URL.

    Notes
    -----
    For PDF files, this function uses pypdf to extract text.
    For web pages, it uses the browser_scrape function for extraction.
    """
    async with session.get(url, allow_redirects=True) as response:
        if response.status == 200:
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/pdf" in content_type:
                # Handle PDF content
                pdf_content = await response.read()
                pdf_file = io.BytesIO(pdf_content)
                try:
                    # Use pypdf to read the PDF and extract text
                    pdf_reader = PdfReader(pdf_file)
                    text = "\n".join(page.extract_text() for page in pdf_reader.pages)
                    return text
                except Exception as e:
                    logging.error(f"Error extracting text from PDF: {e}")
            else:
                # For non-PDF content, use browser_scrape to extract text
                return await browser_scrape(url)
        else:
            # Log a warning if the download fails
            logging.warning(
                f"Failed to download content from {url}. Status code: {response.status}"
            )
            return None
