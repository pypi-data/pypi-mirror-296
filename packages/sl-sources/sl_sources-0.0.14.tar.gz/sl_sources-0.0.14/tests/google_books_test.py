from typing import Dict, List, Type
import pytest

from sl_sources.google_books import (
    search_google_books,
    download_from_google_books,
    search_and_download_from_google_books,
)
from sl_sources.models import (
    ENTITY_TYPES,
    SOURCE_TYPES,
    WORK_TYPES,
    Author,
    Entity,
    Publication,
    Publisher,
    SearchInput,
    Work,
)
from sl_sources.serialization import serialize_entity_array

@pytest.mark.asyncio
async def test_search_google_books():
    query: str = "Artificial Intelligence"
    num_results: int = 5
    search_input: SearchInput = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.GOOGLE_BOOKS,
        entity_types=[
            ENTITY_TYPES.WORK,
            ENTITY_TYPES.AUTHOR,
            ENTITY_TYPES.PUBLICATION,
            ENTITY_TYPES.PUBLISHER,
        ],
    )

    results = await search_google_books(search_input)

    serialize_entity_array(results, "google_books_search_results.json")

    assert len(results) > 0
    for result in results:
        assert isinstance(result, (Work, Author, Publication, Publisher))
        if isinstance(result, Work):
            assert result.work_type == WORK_TYPES.BOOK
            assert result.source_type == SOURCE_TYPES.GOOGLE_BOOKS

    print("search_google_books test passed!")

@pytest.mark.asyncio
async def test_download_from_google_books():
    # Use a known book ID for testing
    book_id = "zyTCAlFPjgYC"  # This is the ID for "The Hitchhiker's Guide to the Galaxy"
    work = Work(
        id=book_id,
        name="Test Book",
        url=f"https://www.googleapis.com/books/v1/volumes/{book_id}",
        source_type=SOURCE_TYPES.GOOGLE_BOOKS,
        work_type=WORK_TYPES.BOOK,
    )

    result = await download_from_google_books(work)

    serialize_entity_array([result], "google_books_download_results.json")

    assert result.full_text
    assert len(result.full_text) > 0
    assert result.abstract
    assert result.authors
    assert result.year
    assert result.publications

    print("download_from_google_books test passed!")

@pytest.mark.asyncio
async def test_search_and_download_from_google_books():
    """
    Run tests for the Google Books search and download functionality.

    This function performs a test search, processes the results, and
    prints out detailed information about the entities found.
    """
    query: str = "Artificial Intelligence"
    num_results: int = 5
    search_input: SearchInput = SearchInput(
        query=query,
        num_results=num_results,
        source_type=SOURCE_TYPES.GOOGLE_BOOKS,
        entity_types=[
            ENTITY_TYPES.WORK,
            ENTITY_TYPES.AUTHOR,
            ENTITY_TYPES.PUBLICATION,
            ENTITY_TYPES.PUBLISHER,
        ],
    )

    print(f"Searching for '{query}' with a limit of {num_results} results...")

    # Perform the search and download operation
    entities: List[Entity] = await search_and_download_from_google_books(search_input)

    serialize_entity_array(entities, "google_books_search_and_download_results.json")

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
    required_types: List[Type] = [Work, Author, Publication, Publisher]
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
            print(f"  Abstract length: {len(entity.abstract) if entity.abstract else 0}")
            print(f"  Full text length: {len(entity.full_text) if entity.full_text else 0}")
            print(f"  Publications: {', '.join(pub.name for pub in entity.publications)}")

    print("\nTest completed successfully!")