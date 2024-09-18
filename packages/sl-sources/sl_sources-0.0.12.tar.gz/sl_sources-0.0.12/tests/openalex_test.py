import json
from typing import Dict, List, Type

import pytest
from sl_sources.http import ThrottledClientSession

from sl_sources.models import (
    ENTITY_TYPES,
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
from sl_sources.openalex import (
    download_from_openalex,
    search_and_download_from_openalex,
    search_openalex,
)
from sl_sources.serialization import serialize_entity_array
from sl_sources.user_agent import get_user_agent_header


@pytest.mark.asyncio
async def test_search_openalex():
    query = "Artificial Intelligence"
    num_results = 2
    search_input = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.OPENALEX,
        entity_types=[
            ENTITY_TYPES.WORK,
            ENTITY_TYPES.AUTHOR,
            ENTITY_TYPES.INSTITUTION,
            ENTITY_TYPES.PUBLICATION,
            ENTITY_TYPES.PUBLISHER,
        ],
    )

    results = await search_openalex(search_input)

    assert len(results) > 0

    serialize_entity_array(results, "openalex_search_results.json")

    print("search_openalex test passed!")


@pytest.mark.asyncio
async def test_download_from_openalex():
    url = "https://doi.org/10.1038/nature14539"
    work = Work(
        name="test",
        url=url,
        source_type=SOURCE_TYPES.OPENALEX,
        work_type=WORK_TYPES.PAPER,
    )

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        result = await download_from_openalex(work, session)

    assert result.full_text
    assert len(result.full_text) > 0

    serialize_entity_array([result], "openalex_download_results.json")

    print("download_from_openalex test passed!")


@pytest.mark.asyncio
async def test_search_and_download_from_openalex():
    """
    Run a test search and download operation using OpenAlex.

    This function performs a sample search for "Artificial Intelligence",
    processes the results, and prints detailed information about the
    entities found.

    Notes
    -----
    This function is primarily used for testing and demonstrating the
    functionality of the OpenAlex search and download pipeline.
    """
    query = "Artificial Intelligence"
    num_results = 5
    search_input = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.OPENALEX,
        entity_types=[
            ENTITY_TYPES.WORK,
            ENTITY_TYPES.AUTHOR,
            ENTITY_TYPES.INSTITUTION,
            ENTITY_TYPES.PUBLICATION,
            ENTITY_TYPES.PUBLISHER,
        ],
    )

    print(f"Searching for '{query}' with a limit of {num_results} results...")
    entities = await search_and_download_from_openalex(search_input)

    serialize_entity_array(entities, "openalex_search_and_download_results.json")

    print(f"Received {len(entities)} entities.")

    # Check entity types and count
    entity_counts: Dict[str, int] = {}
    for entity in entities:
        entity_type = type(entity).__name__
        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

    print("\nEntity types and counts:")
    for entity_type, count in entity_counts.items():
        print(f"{entity_type}: {count}")

    # Check for required entity types
    required_types: List[Type[Entity]] = [Work, Author, Institution, Publication]
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
            print(
                f"  Associated Publications: {', '.join(pub.name for pub in entity.publications)}"
            )

    print("\nTest completed successfully!")
