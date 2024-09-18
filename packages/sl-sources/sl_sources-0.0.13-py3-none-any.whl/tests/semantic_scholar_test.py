from typing import Dict

import pytest
from sl_sources.http import ThrottledClientSession

from sl_sources.models import (
    SOURCE_TYPES,
    WORK_TYPES,
    Author,
    Institution,
    Publication,
    Publisher,
    SearchInput,
    Work,
)
from sl_sources.semantic_scholar import (
    download_from_semantic_scholar,
    search_and_download_from_semantic_scholar,
    search_semantic_scholar,
)
from sl_sources.serialization import serialize_entity_array
from sl_sources.user_agent import get_user_agent_header


@pytest.mark.asyncio
async def test_search_semantic_scholar():
    query = "Artificial Intelligence"
    num_results = 2
    search_input = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
        entity_types=["work", "author", "publication"],
    )

    results = await search_semantic_scholar(search_input)

    serialize_entity_array(results, "semantic_scholar_search_results.json")

    for result in results:
        assert isinstance(result, (Work, Author, Publication, Institution, Publisher))

    print("search_semantic_scholar test passed!")


@pytest.mark.asyncio
async def test_download_semantic_scholar():
    url = "https://www.semanticscholar.org/paper/Attention-Is-All-You-Need-Vaswani-Shazeer/204e3073870fae3d05bcbc2f6a8e263d9b72e776"
    work = Work(
        name="Test work",
        url=url,
        source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
        work_type=WORK_TYPES.ARTICLE,
    )

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        result = await download_from_semantic_scholar(work, session)

    assert result.full_text
    assert len(result.full_text) > 0

    serialize_entity_array([result], "semantic_scholar_download_results.json")

    print("download_semantic_scholar test passed!")


@pytest.mark.asyncio
async def test_search_and_download_from_semantic_scholar():
    """
    Run a test search and download operation using Semantic Scholar.

    This function performs a sample search for "Artificial Intelligence",
    processes the results, and prints detailed information about the
    entities found.
    """
    print("Starting test for search_and_download function...")

    query = "Artificial Intelligence"
    num_results = 1
    search_input = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.SEMANTIC_SCHOLAR,
        entity_types=["work", "author", "publication"],
    )

    print(f"Searching for '{query}' with a limit of {num_results} results...")
    entities = await search_and_download_from_semantic_scholar(search_input)

    print(f"Received {len(entities)} entities.")

    serialize_entity_array(
        entities, "semantic_scholar_search_and_download_results.json"
    )

    # Check entity types and count
    entity_counts: Dict[str, int] = {}
    for entity in entities:
        entity_type = type(entity).__name__
        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

    print("\nEntity types and counts:")
    for entity_type, count in entity_counts.items():
        print(f"{entity_type}: {count}")

    # Check for required entity types
    required_types = [Work, Author, Publication]
    for required_type in required_types:
        if required_type.__name__ not in entity_counts:
            print(f"Warning: No {required_type.__name__} entities found")

    # Print details of each entity
    for entity in entities:
        print(f"\n{type(entity).__name__}:")
        print(f"  ID: {entity.id}")
        print(f"  Name: {entity.name}")
        if isinstance(entity, Work):
            print(f"  URL: {entity.url}")
            print(f"  Authors: {', '.join(author.name for author in entity.authors)}")
            print(f"  Year: {entity.year}")
            print(f"  DOI: {entity.doi}")
            print(
                f"  Abstract length: {len(entity.abstract) if entity.abstract else 0}"
            )
            print(
                f"  Full text length: {len(entity.full_text) if entity.full_text else 0}"
            )

    print("\nTest completed successfully!")
