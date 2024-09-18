import io
import json
import ssl
import traceback
import uuid
from typing import Any, Dict, List, Optional

import aiohttp
import pyalex
from pyalex import Authors, Institutions, Sources, Works
from pypdf import PdfReader
from .papers import get_paper_details

from .models import (
    ENTITY_TYPES,
    INSTITUTION_TYPES,
    PUBLICATION_TYPES,
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

from .http import ThrottledClientSession, validate_url
from .scrape import browser_scrape
from .google import search_google
from .user_agent import get_user_agent_header

import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def _parse_openalex_id(openalex_id: str) -> str:
    """
    Parse OpenAlex ID and return a string representation of UUID.

    Parameters
    ----------
    openalex_id : str
        The OpenAlex ID to parse.

    Returns
    -------
    str
        A string representation of the UUID generated from the OpenAlex ID.

    Notes
    -----
    This function extracts the last part of the OpenAlex ID and uses it to generate
    a UUID5 using the URL namespace.
    """
    id_part = openalex_id.split("/")[-1]
    return str(uuid.uuid5(uuid.NAMESPACE_URL, id_part))

def try_get_url(entity: Dict[str, Any]) -> Optional[str]:
    """
    Try to get the URL from the entity.

    Parameters
    ----------
    entity : Dict[str, Any]
        The dictionary containing the entity data from OpenAlex.
    """
    url = (
        entity.get("open_access", {}).get("oa_url")
        or entity.get("")
        or entity.get("primary_location", {}).get("pdf_url")
        or entity.get("doi")
        or entity.get("url")
        or entity.get("ids", {}).get("doi")
        or entity.get("ids", {}).get("pmid")
        or entity.get("ids", {}).get("arxiv")
        or entity.get("ids", {}).get("openalex")
    )
    return validate_url(url) if url else None



async def _process_work(entity: Dict[str, Any]) -> Optional[Work]:
    url = try_get_url(entity)

    if "arxiv.org" in url or "biorxiv.org" in url or "pubmed.ncbi.nlm.nih.gov" in url:
        paper_details = await get_paper_details(url)
        if paper_details:
            return Work(
                id=_parse_openalex_id(entity["id"]),
                work_type=paper_details.work_type,
                source_type=paper_details.source_type,
                name=paper_details.name,
                url=paper_details.url,
                abstract=paper_details.abstract,
                full_text=paper_details.full_text,
                year=paper_details.year,
                doi=paper_details.doi,
                authors=paper_details.authors,
                institutions=paper_details.institutions,
                publications=paper_details.publications,
            )

    authors = []
    all_institutions = []

    for author_data in entity.get("authorships", []):
        author = Author(
            id=_parse_openalex_id(author_data["author"].get("id", "")),
            name=author_data["author"].get("display_name", ""),
            source_type=SOURCE_TYPES.OPENALEX,
        )
        author_institutions = [
            Institution(
                id=_parse_openalex_id(inst.get("id", "")),
                name=inst.get("display_name", ""),
                source_type=SOURCE_TYPES.OPENALEX,
                institution_type=INSTITUTION_TYPES.ACADEMIC,
            )
            for inst in author_data.get("institutions", [])
        ]
        author.institutions = author_institutions
        authors.append(author)

        all_institutions.extend(author_institutions)

    work_institutions = [
        Institution(
            id=_parse_openalex_id(inst.get("id", "")),
            name=inst.get("display_name", ""),
            source_type=SOURCE_TYPES.OPENALEX,
            institution_type=INSTITUTION_TYPES.ACADEMIC,
        )
        for inst in entity.get("institutions", [])
    ]

    all_institutions.extend(work_institutions)

    publications = []
    locations = entity.get("locations", [])
    if entity.get("primary_location"):
        locations.insert(0, entity["primary_location"])

    for location in locations:
        if location.get("source"):
            source = location["source"]
            publication_type = _get_publication_type(source.get("type"))
            
            if publication_type == PUBLICATION_TYPES.CONFERENCE_PROCEEDINGS:
                conference = Institution(
                    id=_parse_openalex_id(source.get("id", "")),
                    name=source.get("display_name", ""),
                    source_type=SOURCE_TYPES.OPENALEX,
                    institution_type=INSTITUTION_TYPES.CONFERENCE,
                    url=source.get("homepage_url", None)
                )
                all_institutions.append(conference)
            
            publication = Publication(
                id=_parse_openalex_id(source.get("id", "")),
                name=source.get("display_name", ""),
                source_type=SOURCE_TYPES.OPENALEX,
                publication_type=publication_type,
                url=source.get("homepage_url", ""),
            )
            
            if source.get("host_organization"):
                host_org = source["host_organization"]
                publication.publisher = Publisher(
                    id=_parse_openalex_id(host_org),
                    name=host_org,
                    source_type=SOURCE_TYPES.OPENALEX,
                    url=None,
                    description=None,
                )
            publications.append(publication)

    work_type = WORK_TYPES.PAPER

    try:
        return Work(
            id=_parse_openalex_id(entity["id"]),
            work_type=work_type,
            source_type=SOURCE_TYPES.OPENALEX,
            name=entity.get("title", ""),
            url=validate_url(url),
            abstract=_reconstruct_abstract(entity.get("abstract_inverted_index")),
            full_text="",
            year=entity.get("publication_year"),
            doi=entity.get("doi"),
            authors=authors,
            institutions=all_institutions,
            publications=publications,
        )
    except Exception as e:
        print("Error processing work for ", entity["id"], ": ", e)
        print("Entity is: ", entity)
        return None

def _get_publication_type(type_str: str) -> PUBLICATION_TYPES:
    """
    Map OpenAlex publication types to our PUBLICATION_TYPES enum.

    Parameters
    ----------
    type_str : str
        The publication type string from OpenAlex.

    Returns
    -------
    PUBLICATION_TYPES
        The corresponding PUBLICATION_TYPES enum value.
    """
    type_mapping = {
        "journal": PUBLICATION_TYPES.JOURNAL,
        "repository": PUBLICATION_TYPES.OTHER,
        "conference": PUBLICATION_TYPES.CONFERENCE_PROCEEDINGS,
        "book": PUBLICATION_TYPES.BOOK,
    }
    return type_mapping.get(type_str, PUBLICATION_TYPES.UNKNOWN)


def _process_author(entity: Dict[str, Any]) -> Author:
    """
    Process an author entity from OpenAlex and convert it to an Author object.

    Parameters
    ----------
    entity : Dict[str, Any]
        The dictionary containing the author entity data from OpenAlex.

    Returns
    -------
    Author
        An Author object constructed from the OpenAlex data.

    Notes
    -----
    This function extracts the author's name and associated institutions from
    the OpenAlex data and creates an Author object.
    """
    return Author(
        id=_parse_openalex_id(entity["id"]),
        source_type=SOURCE_TYPES.OPENALEX,
        name=entity.get("display_name"),
        institutions=[
            _process_institution(inst) for inst in entity.get("institutions", [])
        ],
    )


def _process_institution(openalex_entity: Dict[str, Any]) -> Institution:
    """
    Process an institution entity from OpenAlex and convert it to an Institution object.

    Parameters
    ----------
    openalex_entity : Dict[str, Any]
        The dictionary containing the institution entity data from OpenAlex.

    Returns
    -------
    Institution
        An Institution object constructed from the OpenAlex data.

    Notes
    -----
    This function extracts the institution's name and ROR (Research Organization Registry)
    URL from the OpenAlex data and creates an Institution object.
    """
    return Institution(
        id=_parse_openalex_id(openalex_entity["id"]),
        source_type=SOURCE_TYPES.OPENALEX,
        institution_type=INSTITUTION_TYPES.ACADEMIC,
        name=openalex_entity.get("display_name"),
        url=openalex_entity.get("ror"),
    )


def _process_publication(entity: Dict[str, Any]) -> Publication:
    """
    Process a publication entity from OpenAlex and convert it to a Publication object.

    Parameters
    ----------
    entity : Dict[str, Any]
        The dictionary containing the publication entity data from OpenAlex.

    Returns
    -------
    Publication
        A Publication object constructed from the OpenAlex data.

    Notes
    -----
    This function extracts the publication's name and URL (homepage or general URL)
    from the OpenAlex data and creates a Publication object.
    """
    url = try_get_url(entity)
    return Publication(
        id=_parse_openalex_id(entity["id"]),
        source_type=SOURCE_TYPES.OPENALEX,
        publication_type=PUBLICATION_TYPES.JOURNAL,
        name=entity.get("display_name"),
        url=validate_url(url) if url else None,
    )


async def _process_entity(entity: Dict[str, Any], entity_type: str) -> Optional[Entity]:
    """
    Process an entity from OpenAlex based on its type.

    Parameters
    ----------
    entity : Dict[str, Any]
        The dictionary containing the entity data from OpenAlex.
    entity_type : str
        The type of the entity ('work', 'author', 'institution', or 'publication').

    Returns
    -------
    Optional[Entity]
        An Entity object (Work, Author, Institution, or Publication) if processing
        is successful, None otherwise.

    Notes
    -----
    This function serves as a router to call the appropriate processing function
    based on the entity type. It handles unknown entity types by logging a warning
    and returning None.
    """
    if entity_type == "work":
        return await _process_work(entity)
    elif entity_type == "author":
        return _process_author(entity)
    elif entity_type == "institution":
        return _process_institution(entity)
    elif entity_type == "publication":
        return _process_publication(entity)
    else:
        logging.error(f"Error processing {entity_type} entity: {str(entity.type)}")
        logging.error(traceback.format_exc())
        return None


async def _download_and_extract_text(url: str, session: aiohttp.ClientSession) -> str:
    """
    Download content from a URL and extract text, handling both PDFs and web pages.

    Parameters
    ----------
    url : str
        The URL to download content from.
    session : aiohttp.ClientSession
        The aiohttp client session to use for making requests.

    Returns
    -------
    str
        The extracted text content from the URL.

    Raises
    ------
    ValueError
        If the input URL is not a string.
    Exception
        If the download fails or content extraction encounters an error.

    Notes
    -----
    This function attempts to download the content from the given URL. If the content
    is a PDF, it extracts the text using pypdf. For other content types, it uses
    browser_scrape to extract the text.
    """
    if not isinstance(url, str):
        raise ValueError(f"Invalid URL type: {type(url)}. Expected str.")

    async with session.get(url, allow_redirects=True) as response:
        if response.status == 200:
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/pdf" in content_type:
                pdf_content = await response.read()
                pdf_file = io.BytesIO(pdf_content)
                try:
                    pdf_reader = PdfReader(pdf_file)
                    text = "\n".join(page.extract_text() for page in pdf_reader.pages)
                    return text
                except Exception as e:
                    logging.error(f"Error extracting text from PDF: {e}")
            else:
                return await browser_scrape(url)
        else:
            raise Exception(
                f"Failed to download content from {url}. Status code: {response.status}"
            )


def _reconstruct_abstract(
    inverted_index: Optional[Dict[str, List[int]]]
) -> Optional[str]:
    """
    Reconstruct the abstract from an inverted index.

    Parameters
    ----------
    inverted_index : Optional[Dict[str, List[int]]]
        A dictionary where keys are words and values are lists of positions.

    Returns
    -------
    Optional[str]
        The reconstructed abstract as a string, or None if the input is None.

    Notes
    -----
    This function takes an inverted index (where words are keys and their positions
    in the text are values) and reconstructs the original text by placing each word
    in its correct position.
    """
    if not inverted_index:
        return None

    words = []
    max_position = max(max(positions) for positions in inverted_index.values())

    for i in range(max_position + 1):
        for word, positions in inverted_index.items():
            if i in positions:
                words.append(word)
                break

    return " ".join(words)


async def download_from_openalex(work: Work, session: ThrottledClientSession) -> Work:
    """
    Download the full text content for a given work from OpenAlex.

    Parameters
    ----------
    work : Work
        The Work object for which to download the full text.
    session : ThrottledClientSession
        The aiohttp client session to use for making requests.

    Returns
    -------
    Work
        The Work object with the full text content if successfully downloaded, or the original Work object if not.

    Notes
    -----
    This function attempts to download the full text using several methods:
    1. Directly from the work's URL
    2. By searching Google for a PDF of the work
    3. By scraping the work's webpage
    If all methods fail, it returns the original Work object.
    """
    print("Downloading from OpenAlex: ", work)
    if not work.url:
        return work

    try:
        # Attempt to download and extract text from the primary URL
        full_text = await _download_and_extract_text(work.url, session)
        if full_text:
            work.full_text = full_text
            return work
    except Exception as e:
        logging.warning(f"Warning: Could not download full text from primary URL: {e}")

    # If primary URL fails, search Google for a PDF
    search_results = await search_google(
        SearchInput(
            query=work.name,
            file_type="pdf",
            num_results=3,
            source_type=SOURCE_TYPES.OPENALEX,
            entity_types=[ENTITY_TYPES.WORK],
        )
    )
    for search_result in search_results:
        try:
            text = await _download_and_extract_text(search_result.url, session)
            if text:
                work.url = validate_url(search_result.url)
                logging.info(
                    f"Downloaded full text from Google search: {search_result.url}"
                )
                work.full_text = text
                return work
        except Exception as e:
            logging.warn(f"Error downloading PDF from Google search: {e}")

    try:
        # If all else fails, attempt to scrape the text from the webpage
        text = await browser_scrape(str(work.url))
        if text:
            logging.info(f"Downloaded full text from original URL: {work.url}")
            work.full_text = text
            return work
    except Exception as e:
        logging.error(f"Error scraping full text: {e}")

    return work


async def search_and_download_from_openalex(search_input: SearchInput) -> List[Entity]:
    """
    Perform a search on OpenAlex and download full text content for the results.

    Parameters
    ----------
    search_input : SearchInput
        An object containing search parameters such as query, number of results,
        and entity types to search for.

    Returns
    -------
    List[Entity]
        A list of Entity objects (Works, Authors, Institutions, Publications)
        found and processed from the OpenAlex search.

    Notes
    -----
    This function performs a search using the OpenAlex API, processes the results
    into Entity objects, and attempts to download full text content for Work entities.
    It also handles deduplication of publications and ensures all related entities
    (authors, institutions) are included in the results.
    """
    logging.info(f"Starting search with input: {search_input}")
    search_results = await search_openalex(search_input)

    entities: List[Entity] = []
    publications_set = set()  # To keep track of unique publications

    # Process search results and collect all related entities
    for result in search_results:
        logging.info(f"Processing result of type: {result.type}")
        entities.append(result)

        if isinstance(result, Work):
            for author in result.authors:
                if author not in entities:
                    entities.append(author)
                for institution in author.institutions:
                    if institution not in entities:
                        entities.append(institution)

            for institution in result.institutions:
                if institution not in entities:
                    entities.append(institution)

            for publication in result.publications:
                if publication.id not in publications_set:
                    entities.append(publication)
                    publications_set.add(publication.id)

    # Download full text for Work entities
    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        for entity in entities:
            if isinstance(entity, Work):
                try:
                    entity = await download_from_openalex(entity, session)
                except Exception as e:
                    logging.warn(f"Error downloading full text for {entity.name}: {e}")
                    entity.full_text = ""

    logging.info(f"Total entities created: {len(entities)}")
    return entities


async def search_openalex(search_input: SearchInput) -> List[Entity]:
    """
    Perform a search on OpenAlex for various entity types.

    Parameters
    ----------
    search_input : SearchInput
        An object containing search parameters such as query, number of results,
        and entity types to search for.

    Returns
    -------
    List[Entity]
        A list of Entity objects found in the OpenAlex search.

    Notes
    -----
    This function searches OpenAlex for different entity types (work, author,
    institution, publication) based on the search input. It uses the pyalex
    library to interact with the OpenAlex API and processes the results into
    appropriate Entity objects.
    """
    query = search_input.query
    num_results = search_input.num_results
    entity_types = search_input.entity_types

    results = []

    for entity_type in entity_types:
        try:
            logging.info(f"Searching for {entity_type} with query: {query}")
            if entity_type == "work":
                entities = Works().search(query).paginate(per_page=num_results * 2)
            elif entity_type == "author":
                entities = Authors().search(query).paginate(per_page=num_results)
            elif entity_type == "institution":
                entities = Institutions().search(query).paginate(per_page=num_results)
            elif entity_type == "publication":
                entities = Sources().search(query).paginate(per_page=num_results)
            else:
                continue

            entity_results = []
            for page in entities:
                for entity in page:
                    # if entity is none, continue, but why would that be? throw a warning
                    if entity is None:
                        logging.warn(f"Entity is None for {entity_type}")
                        logging.warn(f"Entity data: {entity}")
                        continue
                    try:
                        processed_result = await _process_entity(entity, entity_type)
                        if processed_result:
                            if isinstance(processed_result, Work):
                                url = processed_result.url
                                if "arxiv.org" in url or "biorxiv.org" in url or "medrxiv.org" in url or "pubmed.ncbi.nlm.nih.gov" in url:
                                    # Resolve the paper details using get_paper_details
                                    paper_details = await get_paper_details(url)
                                    if paper_details:
                                        # Update the Work object with the resolved details
                                        processed_result = Work(
                                            id=processed_result.id,
                                            work_type=processed_result.work_type,
                                            source_type=paper_details.source_type,
                                            name=paper_details.name,
                                            url=paper_details.url,
                                            abstract=paper_details.abstract,
                                            full_text=paper_details.full_text,
                                            year=paper_details.year,
                                            doi=paper_details.doi,
                                            authors=paper_details.authors,
                                            institutions=paper_details.institutions,
                                            publications=paper_details.publications,
                                        )
                            entity_results.append(processed_result)
                    except Exception as e:
                        logging.error(f"Error processing {entity_type} entity: {str(e)}")
                        logging.error(traceback.format_exc())
                        continue


                    if len(entity_results) >= num_results:
                        break

                if len(entity_results) >= num_results:
                    break

            logging.info(f"Found {len(entity_results)} results for {entity_type}")
            results.extend(entity_results)

        except pyalex.api.QueryError as e:
            logging.error(f"OpenAlex API query error for {entity_type}: {e}")
        except Exception as e:
            logging.exception(f"Unexpected error in search_openalex for {entity_type}")

    logging.info(f"Total results found: {len(results)}")
    return results
