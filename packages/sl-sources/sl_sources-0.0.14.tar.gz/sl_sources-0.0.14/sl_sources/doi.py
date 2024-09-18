import json
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

from .google import search_google
from .google_scholar import download_from_google_scholar
from .http import ThrottledClientSession
from .models import (ENTITY_TYPES, INSTITUTION_TYPES, PUBLICATION_TYPES,
                     SOURCE_TYPES, WORK_TYPES, Author, Entity, Institution,
                     Publication, Publisher, SearchInput, Work,
                     create_consistent_uuid)
from .papers import likely_pdf
from .user_agent import get_user_agent_header

def _extract_publisher_from_venue(venue: str) -> Optional[str]:
    """
    Attempt to extract publisher information from the venue string.
    This is a simple heuristic and may need to be improved based on the actual data.
    """
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
        if publisher.lower() in venue.lower():
            return publisher

    return None


def _validate_doi(doi: str) -> Optional[str]:
    """
    Validate a DOI by attempting to resolve it using the official DOI proxy.

    This function checks if the given DOI can be resolved by the official DOI proxy.
    If successful, it returns the resolved URL. If not, it returns None, indicating
    an invalid DOI.

    Parameters
    ----------
    doi : str
        The Digital Object Identifier (DOI) to validate.

    Returns
    -------
    Optional[str]
        The URL assigned to the DOI if valid, or None if the DOI is invalid.

    Raises
    ------
    ValueError
        If the DOI is not found (HTTP 404 error).

    Notes
    -----
    This function uses the DOI proxy API to validate and resolve DOIs.
    """
    import json
    import urllib.request
    from urllib.error import HTTPError

    # Construct the URL for the DOI proxy API
    url = f"https://doi.org/api/handles/{doi}"
    backup_url = f"https://doi.org/{doi}"
    print(f"handle url {url}")
    request = urllib.request.Request(url)

    result = None

    try:
        # Attempt to retrieve and parse the JSON response
        result = json.loads(urllib.request.urlopen(request).read().decode())
    except HTTPError:
        # If the DOI is not found, raise a ValueError
        print("HTTP 404: DOI not found")
    
    if result is None:
        try:
            result = json.loads(urllib.request.urlopen(backup_url).read().decode())
        except HTTPError:
            print("HTTP 404: DOI not found")

    if result is None:
        return None

    else:
        try:
            # Extract URLs from the response
            urls = [v["data"]["value"] for v in result["values"] if v.get("type") == "URL"]
            # Return the first URL if available, otherwise None
            return urls[0] if urls else None
        except Exception as e:
            print(f"Error extracting URL: {e}")
            return None


def _get_clean_doi(doi: str) -> str:
    """
    Extract a clean DOI from a string that may contain a DOI or a URL with a DOI.

    This function processes the input string to extract and return a clean DOI.
    It handles both direct DOIs and URLs containing DOIs.

    Parameters
    ----------
    doi : str
        A string containing a DOI or a URL with a DOI.

    Returns
    -------
    str
        The extracted and cleaned DOI.

    Notes
    -----
    This function handles various formats of DOI input, including
    URL-encoded DOIs and DOIs embedded in URLs.
    """
    # Remove any leading or trailing whitespace
    doi = doi.strip()

    # Replace URL-encoded forward slash with actual forward slash
    doi = doi.replace("%2F", "/")

    # Check if the input is a URL containing a DOI
    url_match = re.match(r"https?://(?:dx\.)?doi\.org/(10\.\d+/\S+)$", doi)
    if url_match:
        return url_match.group(1)

    # Check if the input is already a valid DOI
    doi_match = re.match(r"^(10\.\d+/\S+)$", doi)
    if doi_match:
        return doi_match.group(1)

    # If we can't extract a DOI, return the original string
    return doi


def _determine_entity_type(root: ET.Element, namespace: str, doi: str) -> ENTITY_TYPES:
    if root.find(f".//{namespace}journal") is not None:
        return ENTITY_TYPES.PUBLICATION
    elif (
        root.find(f".//{namespace}journal_article") is not None
        or root.find(f".//{namespace}book") is not None
    ):
        return ENTITY_TYPES.WORK
    elif root.find(f".//{namespace}institution") is not None:
        return ENTITY_TYPES.INSTITUTION
    elif root.find(f".//{namespace}person_name") is not None:
        return ENTITY_TYPES.AUTHOR
    elif root.find(f".//{namespace}publisher") is not None:
        return ENTITY_TYPES.PUBLISHER
    else:
        return None


def _parse_crossref_xml(root: ET.Element, doi: str) -> Entity:
    namespace = "{" + root.tag.split("}")[0].split("{")[1] + "}"
    entity_type = _determine_entity_type(root, namespace, doi)

    if entity_type == ENTITY_TYPES.PUBLICATION:
        return _parse_publication(root, doi, namespace)
    elif entity_type == ENTITY_TYPES.WORK:
        return _parse_work(root, doi, namespace)
    elif entity_type == ENTITY_TYPES.INSTITUTION:
        return _parse_institution(root, doi, namespace)
    elif entity_type == ENTITY_TYPES.AUTHOR:
        return _parse_author(root, doi, namespace)
    elif entity_type == ENTITY_TYPES.PUBLISHER:
        return _parse_publisher(root, doi, namespace)
    else:
        return None


def _parse_work(root: ET.Element, doi: str) -> Work:
    """
    Parse XML data for a Work entity.

    Parameters
    ----------
    root : ET.Element
        The root element of the parsed XML.
    doi : str
        The DOI of the work.

    Returns
    -------
    Work
        A Work object populated with data from the XML.

    Notes
    -----
    This function extracts various pieces of information about a scholarly work,
    including its title, abstract, publication year, authors, related publications,
    and affiliated institutions.
    """
    namespace = "{" + root.tag.split("}")[0].split("{")[1] + "}"
    
    title_element = root.find(f".//{namespace}title")
    name = title_element.text if title_element is not None else None

    abstract_element = root.find(f".//{namespace}abstract")
    abstract = abstract_element.text if abstract_element is not None else None

    year_element = root.find(f".//{namespace}published-print/{namespace}year")
    year = int(year_element.text) if year_element is not None else None

    authors = _parse_authors(root)
    publications = _parse_publications(root)
    institutions = _parse_institutions(root, authors)

    return Work(
        doi=doi,
        name=name,
        abstract=abstract,
        year=year,
        authors=authors,
        publications=publications,
        institutions=institutions,
        source_type=SOURCE_TYPES.DOI,
        work_type=WORK_TYPES.PAPER,
    )


def _parse_publication(root: ET.Element, doi: str) -> Publication:
    """
    Parse XML data for a Publication entity.

    Parameters
    ----------
    root : ET.Element
        The root element of the parsed XML.
    doi : str
        The DOI of the publication.

    Returns
    -------
    Publication
        A Publication object populated with data from the XML.

    Notes
    -----
    This function extracts information about a publication, including its title
    and associated publisher.
    """
    # Extract the title of the publication
    title_element = root.find(".//full_title")
    name = title_element.text if title_element is not None else None

    # Parse the publisher information
    publisher = _parse_publisher(root, None)

    # Create and return a Publication object
    return Publication(
        doi=doi, name=name, publisher=publisher, source_type=SOURCE_TYPES.DOI
    )


def _parse_institution(root: ET.Element, doi: str) -> Institution:
    """
    Parse XML data for an Institution entity.

    Parameters
    ----------
    root : ET.Element
        The root element of the parsed XML.
    doi : str
        The DOI of the institution.

    Returns
    -------
    Institution
        An Institution object populated with data from the XML.

    Notes
    -----
    This function extracts the name of the institution from the XML data.
    """
    # Extract the name of the institution
    name_element = root.find(".//organization")
    name = name_element.text if name_element is not None else None

    # Create and return an Institution object
    return Institution(doi=doi, name=name, source_type=SOURCE_TYPES.DOI)


def _parse_author(root: ET.Element, namespace: str) -> Author:
    """
    Parse XML data for an Author entity.

    Parameters
    ----------
    root : ET.Element
        The root element of the parsed XML.

    Returns
    -------
    Author
        An Author object populated with data from the XML.

    Notes
    -----
    This function extracts the author's name by combining their given name and surname.
    """
    # Extract the author's given name and surname
    given_name = root.find(f".//{namespace}given_name")
    surname = root.find(f".//{namespace}surname")
    name = (
        f"{given_name.text} {surname.text}"
        if given_name is not None and surname is not None
        else None
    )

    return Author(name=name, source_type=SOURCE_TYPES.DOI)


def _parse_publisher(root: ET.Element, doi: str) -> Publisher:
    """
    Parse XML data for a Publisher entity.

    Parameters
    ----------
    root : ET.Element
        The root element of the parsed XML.
    doi : str
        The DOI of the publisher.

    Returns
    -------
    Publisher
        A Publisher object populated with data from the XML.

    Notes
    -----
    This function extracts the name of the publisher from the XML data.
    """
    # Extract the name of the publisher
    name_element = root.find(".//publisher")
    name = name_element.text if name_element is not None else None

    # Create and return a Publisher object
    return Publisher(doi=doi, name=name, source_type=SOURCE_TYPES.DOI)


def _parse_authors(root: ET.Element) -> List[Author]:
    """
    Parse all authors from the XML data.

    Parameters
    ----------
    root : ET.Element
        The root element of the parsed XML.

    Returns
    -------
    List[Author]
        A list of Author objects extracted from the XML.

    Notes
    -----
    This function extracts information for all authors mentioned in the XML data.
    """
    authors = []
    # Find all person_name elements in the contributors section
    for person_element in root.findall(".//contributors/person_name"):
        given_name = person_element.find("given_name")
        surname = person_element.find("surname")
        if given_name is not None and surname is not None:
            # Combine given name and surname to form the full name
            name = f"{given_name.text} {surname.text}"
            authors.append(Author(name=name, source_type=SOURCE_TYPES.DOI))
    return authors


def _parse_publications(root: ET.Element) -> List[Publication]:
    """
    Parse all publications from the XML data.

    Parameters
    ----------
    root : ET.Element
        The root element of the parsed XML.

    Returns
    -------
    List[Publication]
        A list of Publication objects extracted from the XML.

    Notes
    -----
    This function extracts information about the journal or publication in which
    the work appears.
    """
    publications = []
    venue_element = root.find(".//venue")
    
    if venue_element is not None:
        venue_text = venue_element.text
        if venue_text:
            publisher_name = _extract_publisher_from_venue(venue_text)
            publisher = None
            if publisher_name:
                publisher = Publisher(
                    id=create_consistent_uuid(publisher_name),
                    name=publisher_name,
                    source_type=SOURCE_TYPES.DOI,
                )
            
            publication = Publication(
                id=create_consistent_uuid(venue_text),
                name=venue_text,
                source_type=SOURCE_TYPES.DOI,
                publication_type=PUBLICATION_TYPES.JOURNAL,
                publisher=publisher,
            )
            publications.append(publication)
    
    return publications


def _parse_institutions(root: ET.Element, authors: List[Author]) -> List[Institution]:
    """
    Parse all institutions from the XML data.

    Parameters
    ----------
    root : ET.Element
        The root element of the parsed XML.

    Returns
    -------
    List[Institution]
        A list of Institution objects extracted from the XML.

    Notes
    -----
    This function extracts information about all institutions mentioned in the XML data.
    """
    institutions = []
    seen_institutions = set()

    for author in authors:
        affiliation_elements = root.findall(
            f".//{{*}}contributor[{{*}}name='{author.name}']/{{*}}affiliation"
        )
        for affiliation_element in affiliation_elements:
            name = affiliation_element.text
            if name and name not in seen_institutions:
                institution = Institution(
                    id=create_consistent_uuid(name),
                    name=name,
                    source_type=SOURCE_TYPES.DOI,
                    institution_type=INSTITUTION_TYPES.ACADEMIC,
                )
                institutions.append(institution)
                seen_institutions.add(name)

    return institutions




async def _fallback_search(
    doi: str, session: ThrottledClientSession
) -> Optional[Entity]:
    """
    Perform a fallback search using Google Scholar and Google when Crossref fails.

    Parameters
    ----------
    doi : str
        The DOI to search for.
    session : ThrottledClientSession
        An active session for making HTTP requests.

    Returns
    -------
    Optional[Entity]
        An Entity object if found through fallback methods, or None if not found.

    Notes
    -----
    This function is used when the primary Crossref lookup fails. It attempts to find
    information about the entity using Google Scholar and then Google if necessary.
    """
    search_query = f'"{doi}"'

    # First, try searching Google Scholar
    search_results = await search_google(
        SearchInput(
            query=search_query,
            num_results=5,
            entity_types=[
                ENTITY_TYPES.WORK,
                ENTITY_TYPES.AUTHOR,
                ENTITY_TYPES.PUBLICATION,
                ENTITY_TYPES.INSTITUTION,
                ENTITY_TYPES.PUBLISHER,
            ],
        )
    )

    # If Google Scholar doesn't return results, fall back to Google search
    if len(search_results) == 0:
        search_results = await search_google(
            SearchInput(
                query=search_query,
                num_results=5,
                entity_types=[
                    ENTITY_TYPES.WORK,
                    ENTITY_TYPES.AUTHOR,
                    ENTITY_TYPES.PUBLICATION,
                    ENTITY_TYPES.INSTITUTION,
                    ENTITY_TYPES.PUBLISHER,
                ],
            )
        )

    # Check if any of the search results match the DOI we're looking for
    for result in search_results:
        # if result.type is Work or Publication, set the doi attribute
        if (
            result.type in [ENTITY_TYPES.WORK, ENTITY_TYPES.PUBLICATION]
            and result.doi == doi
        ):
            return result

    # If no exact match is found, return the first result (if any) and set its DOI
    if search_results:
        result = search_results[0]
        if result.type in [ENTITY_TYPES.WORK, ENTITY_TYPES.PUBLICATION]:
            result.doi = doi
        return result

    # If no results are found, return None
    return None


async def _resolve_entity_url(
    entity: Entity, doi: str, session: ThrottledClientSession
) -> Entity:
    """
    Attempt to resolve a URL to the full content of the entity.

    Parameters
    ----------
    entity : Entity
        The entity to resolve the URL for.
    doi : str
        The DOI of the entity.
    session : ThrottledClientSession
        An active session for making HTTP requests.

    Returns
    -------
    Entity
        The input entity with the url attribute potentially updated.

    Notes
    -----
    This function tries various methods to find a URL for the full content
    of the entity. For Work entities, it attempts to find a PDF link, first
    using Sci-Hub and then through a Google search. For other entity types,
    it uses the standard DOI URL.
    """
    if isinstance(entity, Work):
        # Try to find a PDF URL for Work entities
        sci_hub_url = f"https://sci.bban.top/pdf/{doi}.pdf"
        async with session.get(sci_hub_url, allow_redirects=True) as r:
            if r.status == 200 and await likely_pdf(r):
                entity.url = sci_hub_url
                return entity

        # If Sci-Hub fails, try searching Google for a PDF
        search_query = f'"{entity.name}" "{doi}"'
        search_results = await search_google(
            SearchInput(
                query=search_query,
                file_type="pdf",
                num_results=5,
                entity_types=[ENTITY_TYPES.WORK],
            )
        )
        for search_result in search_results:
            async with session.get(search_result.url, allow_redirects=True) as r:
                if r.status == 200 and await likely_pdf(r):
                    entity.url = search_result.url
                    return entity

    # For non-Work entities or if no PDF is found, use the standard DOI URL
    entity.url = f"https://doi.org/{doi}"
    return entity


async def entity_from_doi(
    doi_url_or_doi: str, resolve_url: bool = False
) -> Optional[Entity]:
    """
    Resolve a DOI to obtain detailed information about the associated entity.

    This function is the core of the DOI resolution process. It attempts to resolve a DOI
    using various methods, including querying the Crossref API and falling back to
    Google Scholar and Google search if necessary. It can optionally resolve the URL
    to full content of the entity.

    Parameters
    ----------
    doi_url_or_doi : str
        A DOI, URL containing a DOI, or a DOI URL.
    resolve_url : bool, optional
        Whether to attempt to resolve a URL to the full content (default is False).

    Returns
    -------
    Optional[Entity]
        An Entity object (Work, Publication, Institution, Author, or Publisher)
        containing details about the resolved DOI, or None if resolution fails.

    Notes
    -----
    This function uses a series of fallback methods to ensure the highest possible
    success rate in resolving DOIs. It first attempts to use the Crossref API, which
    is the most authoritative source. If that fails, it falls back to searching
    Google Scholar and then Google for information about the DOI.

    The function also handles URL resolution for full-text content when requested,
    which is particularly useful for academic papers.
    """
    print("entity_from_doi called with:", doi_url_or_doi)
    # Clean and validate the input DOI
    doi = _get_clean_doi(doi_url_or_doi)
    validated_doi = _validate_doi(doi)
    if validated_doi is None:
        print(f"Invalid DOI: {doi}")
        return None

    print(f"Validated DOI: {validated_doi}")

    entity = None
    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        # Attempt to resolve the DOI using Crossref
        crossref_url = f"https://doi.org/{doi}"
        print(f"Crossref URL: {crossref_url}")

        async with session.get(
            crossref_url, headers={"Accept": "application/vnd.crossref.unixsd+xml"}
        ) as response:
            if response.status == 200:
                data = await response.text()
                # if data includes <!DOCTYPE html or <html, then it's not XML
                if "<!DOCTYPE html" in data or "<html" in data:
                    entity = None
                else:
                    try:
                        root = ET.fromstring(data)
                        entity = _parse_crossref_xml(root, doi)
                    except ET.ParseError as e:
                        print(f"XML parsing error: {e}")
                        entity = None

                if entity is None:
                    entity = await _fallback_search(doi, session)

                if entity is None:
                    print(f"Error: Unable to resolve DOI: {doi}")
                    return None

                if resolve_url and not isinstance(entity, Author):
                    entity = await _resolve_entity_url(entity, doi, session)

    if isinstance(entity, Author):
        entity.id = create_consistent_uuid(entity.name)

    return entity


async def search_doi(search_input: SearchInput) -> List[Entity]:
    """
    Search for entities using DOIs based on a given search input.

    Parameters
    ----------
    search_input : SearchInput
        An object containing the search query and other search parameters.

    Returns
    -------
    List[Entity]
        A list of Entity objects representing the search results.

    Notes
    -----
    This function performs a Google search for DOIs related to the given query,
    then attempts to resolve each DOI to obtain detailed entity information.
    It can return various types of entities (Work, Publication, Institution, etc.).
    """
    # Construct a search query that targets DOIs on doi.org
    search_query = f'"{search_input.query}" site:doi.org'

    # Perform a Google search with the constructed query
    search_results = await search_google(
        SearchInput(
            query=search_query,
            num_results=search_input.num_results,
            source_type="doi",
            entity_types=[
                ENTITY_TYPES.WORK,
                ENTITY_TYPES.AUTHOR,
                ENTITY_TYPES.PUBLICATION,
                ENTITY_TYPES.INSTITUTION,
                ENTITY_TYPES.PUBLISHER,
            ],
        )
    )

    doi_results = []
    for result in search_results:
        if "doi.org" in result.url:
            print(f"Processing URL: {result.url}")
            # Attempt to resolve each DOI
            resolved_entity = await entity_from_doi(result.url)
            if resolved_entity:
                doi_results.append(resolved_entity)
            else:
                print(f"Unable to resolve DOI: {result.url}")

    return doi_results


async def download_from_doi(search_result: Entity) -> Optional[Entity]:
    """
    Download full content for a given entity using its DOI.

    Parameters
    ----------
    doi_url_or_doi : str
        A string containing a DOI or doi.org URL to resolve and download.

    Returns
    -------
    Optional[Entity]
        An Entity object with full content if successful, or None if download fails.

    Notes
    -----
    This function attempts to resolve the DOI of an entity and download its full content.
    It first resolves the DOI to get detailed information about the entity,
    then attempts to download the full content from available sources.
    For Work entities, it uses Google Scholar for full-text download.
    """
    doi = search_result.url
    # if 'doi' exists in the search_result as an attribute and a value, use it
    if hasattr(search_result, "doi") and search_result.doi:
        doi = search_result.doi
    # Resolve the DOI to get detailed information
    resolved_entity = await entity_from_doi(doi, resolve_url=True)
    if resolved_entity is None:
        print(f"Unable to resolve DOI: {doi}")
        return None

    resolved_entity.source_type = SOURCE_TYPES.DOI

    # if resolved_entity is a work and contains full text, return it
    if isinstance(resolved_entity, Work) and resolved_entity.full_text:
        return resolved_entity

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        try:
            if isinstance(resolved_entity, Work):
                # For Work entities, attempt to download full text using Google Scholar
                return await download_from_google_scholar(resolved_entity, session)
            else:
                return resolved_entity
        except Exception as e:
            print(f"Error downloading from DOI: {e}")
            return resolved_entity


async def search_and_download_doi(search_input: SearchInput) -> List[Entity]:
    """
    Search for entities using DOIs and download their full content.

    Parameters
    ----------
    search_input : SearchInput
        An object containing the search query and other search parameters.

    Returns
    -------
    List[Entity]
        A list of Entity objects with full content, representing the search and download results.

    Notes
    -----
    This function combines the functionality of search_doi and download_from_doi
    to provide a complete search and download pipeline. It also creates linkages
    between related entities (e.g., linking Works to their Publications and Authors).
    """
    # Search for DOIs related to the query
    doi_results = await search_doi(search_input)

    entities: Dict[str, Entity] = {}
    for doi_result in doi_results:
        # Attempt to download full content for each found entity
        full_entity = await download_from_doi(doi_result)
        if full_entity:
            entities[full_entity.doi] = full_entity

    # Create linkages between entities
    for entity in entities.values():
        if isinstance(entity, Work):
            # Link Work to its Publications, Institutions, and Authors
            entity.publications = [
                entities[pub.doi] for pub in entity.publications if pub.doi in entities
            ]
            entity.institutions = [
                entities[inst.doi]
                for inst in entity.institutions
                if inst.doi in entities
            ]
            entity.authors = [
                entities[author.doi]
                for author in entity.authors
                if author.doi in entities
            ]
        elif isinstance(entity, Publication):
            # Link Publication to its Publisher
            if entity.publisher and entity.publisher.doi in entities:
                entity.publisher = entities[entity.publisher.doi]

    return list(entities.values())
