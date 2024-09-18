import io
import os
import traceback
from typing import Any, Dict, List, Optional

from pypdf import PdfReader

from .doi import entity_from_doi
from .google import search_google
from .http import ThrottledClientSession
from .models import (ENTITY_TYPES, INSTITUTION_TYPES, PUBLICATION_TYPES,
                     SOURCE_TYPES, WORK_TYPES, Author, Entity, Institution,
                     Publication, Publisher, SearchInput, Work,
                     create_consistent_uuid)
from .scrape import browser_scrape
from .user_agent import get_user_agent_header


async def search_and_download_from_semantic_scholar(
    search_input: SearchInput,
) -> List[Entity]:
    """
    Search Semantic Scholar and download full text content for the search results.

    This function performs a search on Semantic Scholar, processes the results,
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
    This function uses a rate-limited client session to respect Semantic Scholar's
    usage policies. It also handles deduplication of publications and resolution of DOIs.
    """
    search_results = await search_semantic_scholar(search_input)

    entities: List[Entity] = []
    publications_set = set()  # To keep track of unique publications

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        for result in search_results:
            if isinstance(result, Work):
                if result.doi:
                    print("*** Entity from DOI:")
                    print(result)
                    # Resolve DOI to get more reliable data, especially URLs
                    resolved_data = await entity_from_doi(result.doi)
                    print("resolved_data", resolved_data)
                    if resolved_data:
                        result.url = resolved_data.url or result.url
                        # its possible that the returned entity is not a work
                        # in that case, we should just use the original entity
                        if not isinstance(resolved_data, Work):
                            # check if its a publication, author, or institution and append to entities
                            entities.append(resolved_data)
                        else:
                            result.abstract = resolved_data.abstract or result.abstract
                            result.year = resolved_data.year or result.year
                            if resolved_data.authors:
                                result.authors = resolved_data.authors

                            if resolved_data.publications:
                                for publication in resolved_data.publications:
                                    result.publications.append(publication)
                                    if publication.id not in publications_set:
                                        entities.append(publication)
                                    publications_set.add(publication.id)
                entities.append(result)
            elif isinstance(result, Author):
                entities.append(result)
            elif isinstance(result, Publication):
                if result.id not in publications_set:
                    entities.append(result)
                    publications_set.add(result.id)

        downloaded_entites = []

        # Download full text for Work entities
        for entity in entities:
            if isinstance(entity, Work):
                try:
                    downloaded_entity = await download_from_semantic_scholar(
                        entity, session
                    )
                    downloaded_entites.append(downloaded_entity)
                except Exception as e:
                    print(f"Error downloading full text for {entity.name}: {e}")
                    downloaded_entites.append(entity)

    return downloaded_entites


async def search_semantic_scholar(search_input: SearchInput) -> List[Entity]:
    query: str = search_input.query
    num_results: int = search_input.num_results
    entity_types: List[str] = search_input.entity_types
    results: List[Entity] = []

    for entity_type in entity_types:
        if entity_type == ENTITY_TYPES.WORK:
            endpoint = "https://api.semanticscholar.org/graph/v1/paper/search"
            params: Dict[str, Any] = {
                "query": query,
                "fields": ",".join(
                    [
                        "paperId",
                        "title",
                        "year",
                        "authors.name",
                        "authors.affiliations",
                        "citationStyles",
                        "externalIds",
                        "url",
                        "openAccessPdf",
                        "isOpenAccess",
                        "tldr",
                        "venue",
                        "publicationVenue",
                        "journal",
                    ]
                ),
                "limit": num_results,
                "offset": 0,
            }
        elif entity_type == ENTITY_TYPES.AUTHOR:
            endpoint = "https://api.semanticscholar.org/graph/v1/author/search"
            params = {
                "query": query,
                "fields": ",".join(
                    ["authorId", "name", "affiliations", "externalIds", "url"]
                ),
                "limit": num_results,
                "offset": 0,
            }
        else:
            continue

        ssheader = get_user_agent_header()
        ssheader["x-api-key"] = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")

        async with ThrottledClientSession(
            rate_limit=15 / 60, headers=ssheader
        ) as ss_session:
            async with ss_session.get(url=endpoint, params=params) as response:
                if response.status != 200:
                    raise Exception(
                        f"Error searching {entity_type}: {response.status} {response.reason} {await response.text()}"
                    )
                data = await response.json()
                items = data.get("data", [])

        for item in items:
            if entity_type == ENTITY_TYPES.WORK:
                tldr = item.get("tldr", {})
                abstract = tldr.get("text", "") if tldr else ""

                try:
                    # Process authors and their institutions
                    authors = []
                    institutions = []
                    for author_data in item.get("authors", []):
                        author_institutions = []
                        for affiliation in author_data.get("affiliations", []):
                            institution = Institution(
                                id=create_consistent_uuid(affiliation),
                                name=affiliation,
                                source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
                                institution_type=INSTITUTION_TYPES.ACADEMIC,
                            )
                            author_institutions.append(institution)
                            if institution not in institutions:
                                institutions.append(institution)

                        author = Author(
                            id=create_consistent_uuid(
                                author_data.get("authorId", author_data["name"])
                            ),
                            name=author_data["name"],
                            source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
                            institutions=author_institutions,
                        )
                        authors.append(author)

                    # Process publication and publisher
                    publication = None
                    publisher = None
                    venue = (
                        item.get("journal")
                        or item.get("publicationVenue")
                        or item.get("venue")
                    )
                    print("venue ***", venue)
                    if venue and 'name' in venue:
                        # Try to extract publisher from venue information
                        publisher_name = _extract_publisher_from_venue(venue)
                        if publisher_name:
                            publisher = Publisher(
                                id=create_consistent_uuid(publisher_name),
                                name=publisher_name,
                                source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
                            )

                        

                        publication = Publication(
                            id=create_consistent_uuid(venue['name']),
                            name=venue['name'],
                            source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
                            publication_type=PUBLICATION_TYPES.JOURNAL,
                            publisher=publisher,
                        )

                    work = Work(
                        id=create_consistent_uuid(item["paperId"]),
                        work_type=WORK_TYPES.PAPER,
                        name=item["title"],
                        url=item.get("url", ""),
                        abstract=abstract,
                        full_text="",
                        year=item.get("year"),
                        doi=item.get("externalIds", {}).get("DOI"),
                        authors=authors,
                        institutions=institutions,
                        publications=[publication] if publication else [],
                        source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
                    )
                    results.append(work)
                    if publication:
                        results.append(publication)
                    if publisher:
                        results.append(publisher)
                    results.extend(authors)
                    results.extend(institutions)
                except Exception as e:
                    print(f"Error creating work: {e}")
                    print("Erroring Work is", item)
                    # print stacktrace
                    traceback.print_exc()
            elif entity_type == ENTITY_TYPES.AUTHOR:
                author_institutions = []
                for affiliation in item.get("affiliations", []):
                    institution = Institution(
                        id=create_consistent_uuid(affiliation),
                        name=affiliation,
                        source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
                        institution_type=INSTITUTION_TYPES.ACADEMIC,
                    )
                    author_institutions.append(institution)
                    results.append(institution)

                author = Author(
                    id=create_consistent_uuid(item["authorId"]),
                    name=item["name"],
                    source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
                    institutions=author_institutions,
                )
                results.append(author)

    return results


def _extract_publisher_from_venue(venue: str) -> Optional[str]:
    """
    Attempt to extract publisher information from the venue string.
    This is a simple heuristic and may need to be improved based on the actual data.
    """
    print("Extracting from venue", venue)
    # if venue['name'] doesn't exist, skip
    if not venue or 'name' not in venue:
        return None
    # List of known publishers (expand this list as needed)
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
    ]

    for publisher in known_publishers:
        if publisher.lower() in venue['name'].lower():
            return publisher

    return None


async def download_from_semantic_scholar(
    work: Work, session: ThrottledClientSession
) -> Work:
    """
    Download the full text content for a given work from Semantic Scholar.

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
    str
        The full text content of the work if successfully downloaded, or an empty string if not.

    Notes
    -----
    This function tries multiple approaches to obtain the full text:
    1. Direct download from the work's URL
    2. Google search for a PDF of the work
    3. Web scraping of the work's URL
    """
    if not work.url:
        return work

    try:
        full_text = await _download_and_extract_text(work.url, session)
        if full_text:
            work.full_text = full_text
            return work
    except Exception as e:
        print(f"Error downloading full text from primary URL: {e}")

    # If primary URL fails, search Google for a PDF
    search_results = await search_google(
        SearchInput(
            query=f'"{work.name}"',
            source_type=SOURCE_TYPES.GOOGLE,
            file_type="pdf",
            num_results=3,
            entity_types=[ENTITY_TYPES.WORK],
        )
    )
    for search_result in search_results:
        try:
            text = await _download_and_extract_text(search_result.url, session)
            if text:
                work.url = search_result.url
                work.full_text = text
                return work
        except Exception as e:
            print(f"Error downloading PDF from Google search: {e}")

    try:
        # If all else fails, attempt to scrape the text from the webpage
        text = await browser_scrape(work.url)
        if text:
            work.full_text = text
            return work
    except Exception as e:
        print(f"Error scraping full text: {e}")

    return work


async def _download_and_extract_text(url: str, session: ThrottledClientSession) -> str:
    """
    Download content from a URL and extract text, handling both PDFs and web pages.

    This function attempts to download content from a given URL and extract
    text from it. It can handle both PDF files and regular web pages.

    Parameters
    ----------
    url : str
        The URL to download content from.
    session : ThrottledClientSession
        A rate-limited aiohttp client session for making HTTP requests.

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
        if (
            response.status == 200
            and "application/pdf" in response.headers.get("Content-Type", "").lower()
        ):
            content = await response.read()
            pdf_file = io.BytesIO(content)
            pdf_reader = PdfReader(pdf_file)
            return "\n".join(
                page.extract_text() for page in pdf_reader.pages if page.extract_text()
            )
        else:
            return await browser_scrape(url)
