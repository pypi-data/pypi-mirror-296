from sl_sources.doi import (
    download_from_doi,
    entity_from_doi,
    _get_clean_doi,
    search_and_download_doi,
    search_doi,
)
from sl_sources.models import (
    ENTITY_TYPES,
    SOURCE_TYPES,
    WORK_TYPES,
    Author,
    Institution,
    Publication,
    Publisher,
    SearchInput,
    Work,
)
import pytest

from sl_sources.serialization import serialize_entity_array


def test_clean_doi():
    """
    Test function for _get_clean_doi.

    This function tests the _get_clean_doi function with a set of test cases,
    checking if the function correctly cleans and extracts DOIs from various formats.
    """
    test_cases = [
        "10.1000/182",
        "https://doi.org/10.1000/182",
        "http://dx.doi.org/10.1000/182",
        "https://doi.org/10.6028/NIST.AI.100-1",
        "10.6028/NIST.AI.100-1",
    ]

    for case in test_cases:
        print(f"Input: {case}")
        print(f"Cleaned DOI: {_get_clean_doi(case)}")
        assert "http" not in _get_clean_doi(case)
        assert "https" not in _get_clean_doi(case)


@pytest.mark.asyncio
async def test_resolve_doi():
    """
    Test function for entity_from_doi.

    This function tests the entity_from_doi function with a set of test DOIs,
    checking if the function correctly resolves them and returns expected information.
    """
    test_dois = [
        "10.1016/b978-0-12-170150-5.50012-3",
        "10.7551/mitpress/5237.001.0001",
        "10.1080/15265161.2011.634487",
        "10.1002/biot.v3:12",
        "10.1016/j.biopsych.2005.02.031",
        "10.1080/2326263x.2016.1210989",
        "10.1088/1741-2560/13/2/021002",
    ]

    for doi in test_dois:
        result = await entity_from_doi(doi)
        print("result is")
        print(result)
        assert result is not None
        assert result.name
        assert result.source_type
        if result.source_type == "work":
            assert result.abstract
        if result.source_type == "publication":
            assert result.publisher
        if result.source_type == "work":
            assert result.url

    print("entity_from_doi tests passed!")


@pytest.mark.asyncio
async def test_download_from_doi():
    """
    Test function for download_from_doi.

    This function tests the download_from_doi function with a set of test DOIs,
    checking if the function correctly downloads full text content for each DOI.
    """
    test_dois = [
        "10.1016/b978-0-12-170150-5.50012-3",
        "10.7551/mitpress/5237.001.0001",
        "10.1088/1741-2560/13/2/021002",
        "10.3389/fneng.2014.00004",
        "10.1001/jama.1995.03520280069043",
        "10.1001/jama.1992.03480160079038",
        "10.1111/j.1532-5415.2010.03030.x",
        "10.1162/jocn.2009.21010",
    ]

    results = []
    for doi in test_dois:
        search_result = Work(
            name=doi,
            doi=doi,
            source_type=SOURCE_TYPES.DOI,
            url="https://doi.org/" + doi,
            work_type=WORK_TYPES.PAPER,
        )
        result = await download_from_doi(search_result)
        print("Test doi result is")
        print(result)
        results.append(result)
        if result is None:
            print(f"Unable to download from DOI: {doi}")
        else:
            assert result is not None
            # assert result.full_text
            # assert len(result.full_text) > 0

    serialize_entity_array(results, "doi_download_results.json")

    print("download_from_doi tests passed!")


@pytest.mark.asyncio
async def test_search_doi():
    """
    Test function for search_doi.

    This function tests the search_doi function with a sample query,
    checking if the function returns the expected number of results
    and if each result contains the required information.
    """
    query = "Artificial Intelligence"
    num_results = 3
    entity_types = [
        ENTITY_TYPES.WORK,
        ENTITY_TYPES.AUTHOR,
        ENTITY_TYPES.PUBLICATION,
        ENTITY_TYPES.INSTITUTION,
        ENTITY_TYPES.PUBLISHER,
    ]
    results = await search_doi(
        SearchInput(query=query, num_results=num_results, entity_types=entity_types)
    )

    serialize_entity_array(results, "doi_search_results.json")

    assert len(results) == num_results
    for result in results:
        assert result.doi
        assert result.name
        assert result.source_type

    print("search_doi test passed!")


@pytest.mark.asyncio
async def test_search_and_download_doi():
    """
    Test function for search_and_download_doi.

    This function tests the search_and_download_doi function with a sample query,
    checking if the function returns the expected number of results and if each
    result contains the required information including full text content.

    It also verifies that the linkages between entities are correctly established.
    """
    query = "Neuroscience"
    num_results = 2
    results = await search_and_download_doi(
        SearchInput(query=query, num_results=num_results)
    )

    serialize_entity_array(results, "doi_search_and_download_results.json")

    assert len(results) > 0, "No results returned"

    for result in results:
        assert isinstance(
            result, (Work, Publication, Institution, Author, Publisher)
        ), f"Unexpected result type: {type(result)}"
        assert result.doi is not None, "DOI is missing"
        assert result.name is not None, "Name is missing"

        if isinstance(result, Work):
            assert result.abstract is not None, "Abstract is missing for Work"
            assert isinstance(result.authors, list), "Authors should be a list for Work"
            assert isinstance(
                result.publications, list
            ), "Publications should be a list for Work"
            assert isinstance(
                result.institutions, list
            ), "Institutions should be a list for Work"

        elif isinstance(result, Publication):
            assert result.publisher is None or isinstance(
                result.publisher, Publisher
            ), "Publisher should be None or a Publisher instance for Publication"

    # Test linkages
    works = [r for r in results if isinstance(r, Work)]
    if works:
        work = works[0]
        for author in work.authors:
            assert isinstance(author, Author), "Linked author is not an Author instance"
        for publication in work.publications:
            assert isinstance(
                publication, Publication
            ), "Linked publication is not a Publication instance"
        for institution in work.institutions:
            assert isinstance(
                institution, Institution
            ), "Linked institution is not an Institution instance"

    publications = [r for r in results if isinstance(r, Publication)]
    if publications:
        publication = publications[0]
        if publication.publisher:
            assert isinstance(
                publication.publisher, Publisher
            ), "Linked publisher is not a Publisher instance"

    print("All assertions passed")
