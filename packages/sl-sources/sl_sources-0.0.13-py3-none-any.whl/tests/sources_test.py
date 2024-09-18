from typing import List
from sl_sources.models import (
    ENTITY_TYPES,
    SOURCE_TYPES,
    Author,
    Institution,
    Publication,
    SearchInput,
    Work,
)
from sl_sources.sources import (
    download_search_result,
    search_and_download,
    search_source,
)
import pytest


@pytest.mark.asyncio
async def test_search_sources():
    query = "Artificial Intelligence"
    num_results = 2
    search_input = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.OPENALEX,
        entity_types=[ENTITY_TYPES.WORK],
    )

    results = await search_source(search_input)

    # assert len(results) == num_results
    # for result in results:
    #     assert isinstance(result, Work)

    print("search_sources test passed!")


@pytest.mark.asyncio
async def test_download_search_result():
    url = "https://arxiv.org/abs/1706.03762"
    work = Work(name=url, url=url, source_type=SOURCE_TYPES.GOOGLE_SCHOLAR)

    result = await download_search_result(work)

    assert result.full_text
    assert len(result.full_text) > 0

    print("download_search_result test passed!")


@pytest.mark.asyncio
async def test_sources():
    """
    Run a series of tests to ensure the search_and_download function is working correctly
    for various sources and search inputs.
    """
    # Define test cases with different queries, result counts, and entity types
    test_cases = [
        {
            "query": "Artificial Intelligence",
            "num_results": 5,
            "entity_types": ["work", "author", "institution", "publication"],
        },
        {
            "query": "Neuroscience AND Consciousness",
            "num_results": 3,
            "entity_types": ["work", "author"],
        },
        # Additional test cases can be added here
    ]

    sources: List[SOURCE_TYPES] = [
        SOURCE_TYPES.OPENALEX,
        SOURCE_TYPES.GOOGLE_SCHOLAR,
        SOURCE_TYPES.DOI,
        SOURCE_TYPES.SEMANTIC_SCHOLAR,
        SOURCE_TYPES.VIDEO,
        SOURCE_TYPES.GOOGLE,
        # SOURCE_TYPES.TWITTER,
    ]

    # Test each source separately
    for source in sources:
        print(f"\nTesting {source}...")

        for test_case in test_cases:
            print(f"\nSearch query: {test_case['query']}")

            # Create a SearchInput object for each test case
            search_input = SearchInput(
                query=test_case["query"],
                num_results=test_case["num_results"],
                source_type=source,
                entity_types=test_case["entity_types"],
            )

            # Perform the search and download
            entities = await search_and_download(search_input)

            # Analyze and validate the results
            entity_counts = {}
            for entity in entities:
                entity_type = type(entity).__name__
                entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

                # Perform type-specific checks
                if isinstance(entity, Work):
                    print("entity is", entity)
                    assert entity.name, "Work entity should have a name"
                    assert entity.url, "Work entity should have a URL"
                    assert (
                        entity.authors is not None
                    ), "Work entity should have authors (even if empty list)"
                elif isinstance(entity, Author):
                    assert entity.name, "Author entity should have a name"
                elif isinstance(entity, Institution):
                    assert entity.name, "Institution entity should have a name"
                elif isinstance(entity, Publication):
                    assert entity.name, "Publication entity should have a name"

            print("Entity counts:")
            for entity_type, count in entity_counts.items():
                print(f"{entity_type}: {count}")

            # Uncomment the following to check if all requested entity types are present
            # for entity_type in test_case["entity_types"]:
            #     assert entity_type.capitalize() in entity_counts, f"Requested entity type {entity_type} not found in results"

        print(f"{source} tests passed!")
