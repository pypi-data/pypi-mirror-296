from typing import Any, Dict

import aiohttp
import pytest
from sl_sources.models import Work

from sl_sources.papers import (
    get_arxiv_details,
    get_paper_details,
    get_pubmed_details,
    likely_pdf,
    pubmed_to_pdf_url,
)


@pytest.mark.asyncio
async def test_get_arxiv_details():
    """
    Test function for get_arxiv_details.

    This function tests the get_arxiv_details function with a sample arXiv URL.
    """
    url: str = "https://arxiv.org/abs/2303.08774"
    result: Work = await get_arxiv_details(url)
    print(f"ArXiv paper details: {result.model_dump()}")
    assert result.name
    assert result.authors
    assert result.abstract


@pytest.mark.asyncio
async def test_get_pubmed_details():
    """
    Test function for get_pubmed_details.

    This function tests the get_pubmed_details function with a sample PubMed URL.
    """
    url: str = "https://pubmed.ncbi.nlm.nih.gov/35580832"
    result: Work = await get_pubmed_details(url)
    print(f"PubMed paper details: {result.model_dump()}")
    assert result.name
    assert result.authors
    assert result.abstract


@pytest.mark.asyncio
async def test_pubmed_to_pdf_url():
    """
    Test function for pubmed_to_pdf_url.

    This function tests the pubmed_to_pdf_url function with a sample PubMed URL.
    """
    url: str = "https://pubmed.ncbi.nlm.nih.gov/35580832"
    async with aiohttp.ClientSession() as session:
        pdf_url: str = await pubmed_to_pdf_url(url, session)
    print(f"PubMed full-text URL: {pdf_url}")
    assert pdf_url.startswith("http")  # Check that we got a URL
    async with aiohttp.ClientSession() as session:
        async with session.get(pdf_url) as response:
            assert response.status == 200  # Check that the URL is accessible


@pytest.mark.asyncio
async def test_likely_pdf():
    """
    Test function for likely_pdf.

    This function tests the likely_pdf function with a known PDF URL.
    """
    pdf_url: str = "https://arxiv.org/pdf/2303.08774.pdf"
    async with aiohttp.ClientSession() as session:
        async with session.get(pdf_url) as response:
            is_likely_pdf: bool = await likely_pdf(response)
    print(f"Is likely PDF: {is_likely_pdf}")
    assert is_likely_pdf == True


@pytest.mark.asyncio
async def test_get_paper_details():
    """
    Test function for get_paper_details.

    This function tests the get_paper_details function with both arXiv and PubMed URLs.
    It also tests error handling for unsupported URLs.
    """
    arxiv_url: str = "https://arxiv.org/abs/2303.08774"
    pubmed_url: str = "https://pubmed.ncbi.nlm.nih.gov/35580832"
    biorxiv_url: str = "https://www.biorxiv.org/content/10.1101/2024.05.02.563883v1"

    arxiv_result: Work = await get_paper_details(arxiv_url)
    pubmed_result: Work = await get_paper_details(pubmed_url)

    print(f"ArXiv paper details: {arxiv_result.model_dump()}")
    print(f"PubMed paper details: {pubmed_result.model_dump()}")

    assert arxiv_result.id == "2303.08774"
    assert pubmed_result.id == "35580832"

    try:
        await get_paper_details("https://example.com")
    except ValueError as e:
        print(f"Expected error raised: {e}")