import asyncio
import json
import logging
from typing import List

import pytest

from sl_sources.models import ENTITY_TYPES, SOURCE_TYPES, WORK_TYPES, SearchInput, Work
from sl_sources.serialization import serialize_entity_array
from sl_sources.video import (
    download_from_media_site,
    search_and_download_from_media_site,
    search_youtube,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_search_youtube():
    """Test the search_youtube function."""
    query = "Python tutorial"
    num_results = 2
    results = await search_youtube(
        SearchInput(
            query=query,
            num_results=num_results,
            entity_types=[
                ENTITY_TYPES.WORK,
                ENTITY_TYPES.AUTHOR,
                ENTITY_TYPES.INSTITUTION,
                ENTITY_TYPES.PUBLICATION,
                ENTITY_TYPES.PUBLISHER,
            ],
        )
    )

    assert len(results) == num_results

    for result in results:
        assert isinstance(result, Work)
        assert result.name
        assert result.url
        assert result.abstract

    serialize_entity_array(results, "youtube_search_results.json")

    print("Test passed!")


@pytest.mark.asyncio
async def test_download_and_transcribe():
    """Test the download_from_media_site function."""
    video_url_no_captions = Work(
        url="https://www.youtube.com/watch?v=xuCn8ux2gbs",
        name="History of the World, I guess",
        work_type=WORK_TYPES.VIDEO,
        source_type=SOURCE_TYPES.VIDEO,
        entity_types=[
            ENTITY_TYPES.WORK,
            ENTITY_TYPES.AUTHOR,
            ENTITY_TYPES.INSTITUTION,
            ENTITY_TYPES.PUBLICATION,
            ENTITY_TYPES.PUBLISHER,
        ],
    )
    transcript_no_captions = await download_from_media_site(video_url_no_captions)
    assert transcript_no_captions, "Failed to transcribe video"
    print("Successfully transcribed video")

    assert (
        len(transcript_no_captions.full_text.split()) > 100
    ), "Transcript seems too short"

    serialize_entity_array([transcript_no_captions], "youtube_download_results.json")


@pytest.mark.asyncio
async def download_videos_parallel(works: List[Work]) -> List[Work]:
    """Download multiple videos in parallel."""
    tasks = [download_from_media_site(work) for work in works]
    gathered = await asyncio.gather(*tasks)
    return gathered


@pytest.mark.asyncio
async def test_search_and_download_from_media_site():
    """Test the search_and_download_from_media_site function."""
    query = "self introduction"
    num_results = 3
    search_input = SearchInput(
        query=query,
        num_results=num_results,
        entity_types=[ENTITY_TYPES.WORK],
        source_type=SOURCE_TYPES.VIDEO,
    )

    logger.info(f"Starting test with query: {query}, num_results: {num_results}")

    results = await search_and_download_from_media_site(search_input)

    logger.info(f"Received {len(results)} results")

    serialize_entity_array(results, "youtube_search_and_download_results.json")

    assert len(results) > 0, f"Expected at least one result, got {len(results)}"

    for result in results:
        assert isinstance(result, Work), f"Expected Work object, got {type(result)}"
        assert result.name, "Work name is missing"
        assert result.url, "Work URL is missing"
        assert result.abstract, "Work abstract is missing"
        assert result.full_text, "Work full text (transcript) is missing"

    logger.info("Test passed successfully!")
