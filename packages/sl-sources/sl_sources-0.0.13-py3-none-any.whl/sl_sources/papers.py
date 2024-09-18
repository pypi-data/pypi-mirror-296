import re
from typing import Dict, Any, List, Optional
import aiohttp
from bs4 import BeautifulSoup

from sl_sources.models import INSTITUTION_TYPES, PUBLICATION_TYPES, SOURCE_TYPES, WORK_TYPES, Author, Institution, Publication, Work, create_consistent_uuid


async def get_paper_details(url: str) -> Work:
    """
    Get paper details from a given URL.

    This function determines the source of the paper (arXiv, bioRxiv, medRxiv, or PubMed) based on the URL
    and calls the appropriate function to fetch the details.

    Parameters
    ----------
    url : str
        The URL of the paper.

    Returns
    -------
    Work
        A Work object containing the paper details.

    Raises
    ------
    ValueError
        If the URL is not supported (neither arXiv, bioRxiv, medRxiv, nor PubMed).

    Notes
    -----
    This function serves as a router to direct requests to the appropriate
    paper detail fetching function based on the URL structure.
    """
    if "arxiv.org" in url:
        return await get_arxiv_details(url)
    elif "biorxiv.org" in url:
        return await get_biorxiv_details(url)
    elif "medrxiv.org" in url:
        return await get_medrxiv_details(url)
    elif "pubmed.ncbi.nlm.nih.gov" in url:
        return await get_pubmed_details(url)
    else:
        return None
    

async def get_arxiv_details(url: str) -> Work:
    match = re.search(r"(?:arxiv\.org/(?:abs|pdf)/)(.+)", url)
    if match:
        arxiv_id: str = match.group(1)
        if arxiv_id.endswith(".pdf"):
            arxiv_id = arxiv_id[:-4]
    else:
        raise ValueError(f"Unable to extract arXiv ID from URL: {url}")
    api_url: str = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            soup = BeautifulSoup(await response.text(), "lxml-xml")

            entry = soup.find("entry")
            name: str = entry.find("title").text
            abstract: str = entry.find("summary").text

            authors: List[Author] = []
            institutions: List[Institution] = []
            for author_element in entry.find_all("author"):
                author_name: str = author_element.find("name").text
                affiliations: List[str] = [
                    affiliation.text for affiliation in author_element.find_all("affiliation")
                ]
                author_institutions: List[Institution] = []
                for affiliation in affiliations:
                    institution = Institution(
                        id=create_consistent_uuid(affiliation),
                        name=affiliation,
                        source_type=SOURCE_TYPES.OPENALEX,
                        institution_type=INSTITUTION_TYPES.UNKNOWN
                    )
                    author_institutions.append(institution)
                    institutions.append(institution)
                authors.append(Author(
                    id=create_consistent_uuid(author_name),
                    name=author_name,
                    source_type=SOURCE_TYPES.OPENALEX,
                    institutions=author_institutions
                ))

            work = Work(
                id=arxiv_id,
                name=name,
                authors=authors,
                abstract=abstract,
                source_type=SOURCE_TYPES.OPENALEX,
                doi=f"10.48550/arXiv.{arxiv_id}",
                url=f"https://arxiv.org/abs/{arxiv_id}",
                work_type=WORK_TYPES.PAPER,
                institutions=institutions,
                publications=[Publication(
                    id=create_consistent_uuid("arXiv"),
                    name="arXiv",
                    source_type=SOURCE_TYPES.OPENALEX,
                    publication_type=PUBLICATION_TYPES.UNKNOWN,
                    url="https://arxiv.org"
                )]
            )

            return work

async def get_pubmed_details(url: str) -> Work:
    pubmed_id: str = re.search(r"(?:pubmed\.ncbi\.nlm\.nih\.gov/)(\d+)", url).group(1)
    summary_url: str = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pubmed_id}&retmode=json"
    abstract_url: str = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"

    async with aiohttp.ClientSession() as session:
        async with session.get(summary_url) as response:
            summary_data: Dict[str, Any] = await response.json()
            result = summary_data["result"][pubmed_id]

        async with session.get(abstract_url) as response:
            abstract_xml: str = await response.text()
            abstract_soup = BeautifulSoup(abstract_xml, "lxml-xml")
            abstract = abstract_soup.find("AbstractText")
            abstract_text: str = abstract.text if abstract else "Abstract not available"

        name: str = result["title"]
        doi: str = result.get("elocationid", "")

        authors: List[Author] = []
        institutions: List[Institution] = []
        for author_data in result["authors"]:
            author_name: str = author_data["name"]
            affiliations: List[str] = author_data.get("affiliations", [])
            author_institutions: List[Institution] = []
            for affiliation in affiliations:
                institution = Institution(
                    id=create_consistent_uuid(affiliation),
                    name=affiliation,
                    source_type=SOURCE_TYPES.OPENALEX,
                    institution_type=INSTITUTION_TYPES.UNKNOWN
                )
                author_institutions.append(institution)
                institutions.append(institution)
            authors.append(Author(
                id=create_consistent_uuid(author_name),
                name=author_name,
                source_type=SOURCE_TYPES.OPENALEX,
                institutions=author_institutions
            ))

        work = Work(
            id=pubmed_id,
            name=name,
            authors=authors,
            abstract=abstract_text,
            source_type=SOURCE_TYPES.OPENALEX,
            doi=doi,
            url=url,
            work_type=WORK_TYPES.PAPER,
            institutions=institutions,
            publications=[Publication(
                id=create_consistent_uuid("PubMed"),
                name="PubMed",
                source_type=SOURCE_TYPES.OPENALEX,
                publication_type=PUBLICATION_TYPES.UNKNOWN,
                url="https://pubmed.ncbi.nlm.nih.gov"
            )]
        )

        return work


async def get_biorxiv_details(url: str) -> Work:
    biorxiv_id: str = re.search(r"(?:biorxiv\.org/content/)(.+)", url).group(1)
    api_url: str = f"https://api.biorxiv.org/details/{biorxiv_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()

            entry = data["collection"][0]
            name: str = entry["title"]
            abstract: str = entry["abstract"]

            authors: List[Author] = []
            institutions: List[Institution] = []
            for author_data in entry["authors"]:
                author_name: str = author_data["name"]
                affiliations: List[str] = author_data.get("affiliations", [])
                author_institutions: List[Institution] = []
                for affiliation in affiliations:
                    institution = Institution(
                        id=create_consistent_uuid(affiliation),
                        name=affiliation,
                        source_type=SOURCE_TYPES.OPENALEX,
                        institution_type=INSTITUTION_TYPES.UNKNOWN
                    )
                    author_institutions.append(institution)
                    institutions.append(institution)
                authors.append(Author(
                    id=create_consistent_uuid(author_name),
                    name=author_name,
                    source_type=SOURCE_TYPES.OPENALEX,
                    institutions=author_institutions
                ))

            work = Work(
                id=biorxiv_id,
                name=name,
                authors=authors,
                abstract=abstract,
                source_type=SOURCE_TYPES.OPENALEX,
                doi=f"10.1101/{biorxiv_id}",
                url=url,
                work_type=WORK_TYPES.PAPER,
                institutions=institutions,
                publications=[Publication(
                    id=create_consistent_uuid("bioRxiv"),
                    name="bioRxiv",
                    source_type=SOURCE_TYPES.OPENALEX,
                    publication_type=PUBLICATION_TYPES.UNKNOWN,
                    url="https://www.biorxiv.org"
                )]
            )

            return work


async def get_medrxiv_details(url: str) -> Work:
    medrxiv_id: str = re.search(r"(?:medrxiv\.org/content/)(.+)", url).group(1)
    api_url: str = f"https://api.biorxiv.org/details/{medrxiv_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()

            entry = data["collection"][0]
            name: str = entry["title"]
            abstract: str = entry["abstract"]

            authors: List[Author] = []
            institutions: List[Institution] = []
            for author_data in entry["authors"]:
                author_name: str = author_data["name"]
                affiliations: List[str] = author_data.get("affiliations", [])
                author_institutions: List[Institution] = []
                for affiliation in affiliations:
                    institution = Institution(
                        id=create_consistent_uuid(affiliation),
                        name=affiliation,
                        source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                        institution_type=INSTITUTION_TYPES.UNKNOWN
                    )
                    author_institutions.append(institution)
                    institutions.append(institution)
                authors.append(Author(
                    id=create_consistent_uuid(author_name),
                    name=author_name,
                    source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                    institutions=author_institutions
                ))

            work = Work(
                id=medrxiv_id,
                name=name,
                authors=authors,
                abstract=abstract,
                source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                doi=f"10.1101/{medrxiv_id}",
                url=url,
                work_type=WORK_TYPES.PAPER,
                institutions=institutions,
                publications=[Publication(
                    id=create_consistent_uuid("medRxiv"),
                    name="medRxiv",
                    source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
                    publication_type=PUBLICATION_TYPES.UNKNOWN,
                    url="https://www.medrxiv.org"
                )]
            )

            return work

async def pubmed_to_pdf_url(url: str, session: aiohttp.ClientSession) -> str:
    """
    Attempt to find a PDF URL for a given PubMed article.

    This function tries to locate a PDF link for a PubMed article by first checking
    for a PMC ID, and if not found, searching for full-text links on the PubMed page.

    Parameters
    ----------
    url : str
        The PubMed URL of the article.
    session : aiohttp.ClientSession
        An active aiohttp ClientSession for making requests.

    Returns
    -------
    str
        The URL of the PDF if found.

    Raises
    ------
    Exception
        If no full-text link is found or if there's an error fetching the page.

    Notes
    -----
    This function prioritizes PMC (PubMed Central) PDFs if available, otherwise
    it looks for any available full-text links.
    """
    pubmed_id: str = url.split("/")[-1]

    async with session.get(url) as r:
        if r.status != 200:
            raise Exception(
                f"Error fetching page for PubMed ID {pubmed_id}. Status: {r.status}"
            )
        html_text: str = await r.text()
        soup = BeautifulSoup(html_text, "html.parser")

        # First, try to find a PMC ID
        pmc_id_match = re.search(r"PMC\d+", html_text)
        if pmc_id_match:
            pmc_id: str = pmc_id_match.group(0)[3:]
            pdf_url: str = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
            async with session.get(pdf_url) as pdf_r:
                if pdf_r.status == 200:
                    return pdf_url

        # If no PMC ID or PDF not available, look for full-text links
        full_text_links: List[BeautifulSoup] = soup.select(".full-text-links-list a")
        for link in full_text_links:
            href: Optional[str] = link.get("href")
            if href:
                # Prioritize PDF links
                if href.endswith(".pdf") or "pdf" in href.lower():
                    return href
                else:
                    # Return the first available link if no PDF link is found
                    return href

        # If no full-text links are found
        raise Exception(f"No full-text link found for PubMed ID {pubmed_id}.")


async def likely_pdf(response: aiohttp.ClientResponse) -> bool:
    """
    Determine if a given response is likely to be a PDF.

    This function uses various heuristics to determine if the content of an
    HTTP response is likely to be a PDF file.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        The HTTP response to check.

    Returns
    -------
    bool
        True if the response is likely to be a PDF, False otherwise.

    Notes
    -----
    This function checks for common text patterns in the response that might
    indicate it's not a PDF, and also checks the Content-Type header.
    """
    try:
        text: str = await response.text()
        text = text.lower()
        # Check for common patterns that indicate it's not a PDF
        if any(
            phrase in text
            for phrase in [
                "invalid article id",
                "no paper",
                "not found",
                "404",
                "error",
                "403",
                "forbidden",
            ]
        ):
            return False
    except UnicodeDecodeError:
        # If we can't decode the text, it's likely a binary file (possibly a PDF)
        return True

    # Check the Content-Type header
    if response.headers.get("Content-Type") == "application/pdf":
        return True

    return False
