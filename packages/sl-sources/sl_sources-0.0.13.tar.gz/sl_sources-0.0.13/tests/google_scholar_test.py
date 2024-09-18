import asyncio
from typing import Dict, List, Type
import pytest

from sl_sources.google_scholar import (
    search_and_download_from_google_scholar,
    search_google_scholar,
    download_from_google_scholar,
)
from sl_sources.models import (
    ENTITY_TYPES,
    SOURCE_TYPES,
    Author,
    Entity,
    Institution,
    Publication,
    Publisher,
    SearchInput,
    Work,
)
from sl_sources.serialization import serialize_entity_array
from sl_sources.http import ThrottledClientSession
from sl_sources.user_agent import get_user_agent_header


@pytest.mark.asyncio
async def test_search_google_scholar():
    query: str = "Artificial Intelligence"
    num_results: int = 5
    search_input: SearchInput = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
        entity_types=[
            ENTITY_TYPES.WORK,
            ENTITY_TYPES.AUTHOR,
            ENTITY_TYPES.PUBLICATION,
            ENTITY_TYPES.PUBLISHER,
            ENTITY_TYPES.INSTITUTION,
        ],
    )

    results = await search_google_scholar(search_input)

    serialize_entity_array(results, "google_scholar_search_results.json")

    # assert len(results) == num_results
    for result in results:
        assert isinstance(result, (Work, Author, Publication, Publisher, Institution))

    print("search_google_scholar test passed!")


@pytest.mark.asyncio
async def test_download_from_google_scholar():
    url = "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=oR9sCGYAAAAJ&citation_for_view=oR9sCGYAAAAJ:zYLM7Y9cAGgC"
    work = Work(
        name="attention is all you need",
        url=url,
        source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
        year=2017,
    )

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        result = await download_from_google_scholar(work, session)

    assert result.full_text
    assert len(result.full_text) > 0

    serialize_entity_array([result], "google_scholar_download_results.json")

    print("download_from_google_scholar test passed!")


@pytest.mark.asyncio
async def test_search_and_download_from_google_scholar():
    """
    Run tests for the Google Scholar search and download functionality.

    This function performs a test search, processes the results, and
    prints out detailed information about the entities found.
    """
    query: str = "Artificial Intelligence"
    num_results: int = 5
    search_input: SearchInput = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
        entity_types=[
            ENTITY_TYPES.WORK,
            ENTITY_TYPES.AUTHOR,
            ENTITY_TYPES.PUBLICATION,
        ],
    )

    print(f"Searching for '{query}' with a limit of {num_results} results...")

    # Perform the search and download operation
    entities: List[Entity] = await search_and_download_from_google_scholar(search_input)

    serialize_entity_array(entities, "google_scholar_search_and_download_results.json")

    print(f"Received {len(entities)} entities.")

    # Count the occurrences of each entity type
    entity_counts: Dict[str, int] = {}
    for entity in entities:
        entity_type: str = type(entity).__name__
        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

    # Print the count of each entity type
    print("\nEntity types and counts:")
    for entity_type, count in entity_counts.items():
        print(f"{entity_type}: {count}")

    # Check if all required entity types are present in the results
    required_types: List[Type] = [Work, Author, Publication]
    for required_type in required_types:
        if required_type.__name__ not in entity_counts:
            print(f"Warning: No {required_type.__name__} entities found")

    # Print detailed information for each entity
    for entity in entities:
        print(f"\n{type(entity).__name__}:")
        print(f"  ID: {entity.id}")
        print(f"  Name: {entity.name}")
        if isinstance(entity, Work):
            # Print additional details for Work entities
            print(f"  URL: {entity.url}")
            print(f"  Authors: {', '.join(author.name for author in entity.authors)}")
            print(f"  Year: {entity.year}")
            print(
                f"  Abstract length: {len(entity.abstract) if entity.abstract else 0}"
            )
            print(
                f"  Full text length: {len(entity.full_text) if entity.full_text else 0}"
            )

    print("\nTest completed successfully!")
