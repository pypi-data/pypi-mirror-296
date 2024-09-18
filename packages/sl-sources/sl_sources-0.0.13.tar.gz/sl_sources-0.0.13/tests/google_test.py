import asyncio
from typing import List

import pytest
from dotenv import load_dotenv

from sl_sources.google import (
    download_from_google_search,
    search_and_download_from_google,
    search_google,
)
from sl_sources.models import ENTITY_TYPES, SOURCE_TYPES, Entity, SearchInput, Work
from sl_sources.serialization import serialize_entity_array

# Load environment variables from .env file
load_dotenv()

query: str = "Artificial Intelligence"
num_results: int = 2


@pytest.mark.asyncio
async def test_search_google():
    search_input = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.GOOGLE,
        entity_types=[ENTITY_TYPES.WORK],
    )
    search_results = await search_google(search_input)

    assert len(search_results) == num_results
    for result in search_results:
        assert isinstance(result, Work)
        assert result.id
        assert result.name
        assert result.url
        assert result.abstract

    print("search_google test passed!")


@pytest.mark.asyncio
async def test_download_from_google_search():
    # Perform a search and print results
    search_results: List[Work] = await search_google(
        SearchInput(
            query=query,
            num_results=num_results,
            source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
            entity_types=[ENTITY_TYPES.WORK],
        )
    )
    print(f"Search results: {search_results}")

    serialize_entity_array(search_results, "search_results_google.json")

    tasks = [download_from_google_search(work) for work in search_results]
    # Download full text for search results
    downloaded_pages: List[Work] = await asyncio.gather(*tasks)

    serialize_entity_array(downloaded_pages, "download_results_google.json")

    # Perform assertions to verify the results
    assert len(search_results) == num_results
    for result in search_results:
        assert isinstance(result, Work)
        assert result.id
        assert result.name
        assert result.url
        assert result.abstract

    for result in downloaded_pages:
        assert isinstance(result, Work)
        assert result.full_text

    print("search_google and download_from_google_search tests passed!")


@pytest.mark.asyncio
# Test the combined search_and_download_from_google function
async def test_search_and_download_from_google():
    """
    Test the search_and_download_from_google function.

    This function creates a SearchInput object, calls search_and_download_from_google,
    and performs assertions on the results to ensure correct functionality.
    """
    search_input = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.GOOGLE,
        entity_types=[ENTITY_TYPES.WORK],
    )
    entities: List[Entity] = await search_and_download_from_google(search_input)

    serialize_entity_array(entities, "search_anddownload_results_google.json")

    assert len(entities) == num_results
    for entity in entities:
        assert isinstance(entity, Work)
        assert entity.id
        assert entity.name
        assert entity.url
        assert entity.abstract
        assert entity.full_text

    print("search_and_download_from_google test passed!")
