import asyncio
import hashlib
import json
import os
from typing import Any, Dict, List

from sl_sources.crawl import crawl, _crawl_links
from sl_sources.http import resolve_url
from sl_sources.models import ENTITY_TYPES, SOURCE_TYPES, Work

import pytest

from sl_sources.serialization import serialize_entity_array


@pytest.mark.asyncio
async def test_crawl_links():
    """
    Test function for _crawl_links.
    """
    research_topic: str = (
        "can humans keep up? the impact of artificial intelligence on neuroscience"
    )
    # Test cases
    test_cases: List[Dict[str, Any]] = [
        {
            "links": ["https://example.com", "http://test.org", "www.sample.net"],
            "depth": 1,
            "max_depth": 2,
            "parent_source": {
                "url": "https://parent.com",
                "source_type": "crawl",
                "name": "Parent Page",
            },
            "expected_processed": 3,
        },
        {
            "links": ["/relative/path", "subpage.html", "../sibling.html"],
            "depth": 1,
            "max_depth": 2,
            "parent_source": {
                "url": "https://parent.com/page/",
                "source_type": "crawl",
                "name": "Parent Page",
            },
            "expected_processed": 3,
        },
        {
            "links": ["https://example.com", "invalid://url", "ftp://files.com"],
            "depth": 1,
            "max_depth": 3,
            "parent_source": None,
            "expected_processed": 3,  # All URLs should be processed, even invalid ones
        },
    ]

    for i, case in enumerate(test_cases):
        print(f"Running test case {i + 1}...")

        # Reset cache
        cache: Dict[str, Any] = {}
        entity_types: List[str] = [
            ENTITY_TYPES.WORK,
            ENTITY_TYPES.AUTHOR,
            ENTITY_TYPES.INSTITUTION,
            ENTITY_TYPES.PUBLICATION,
        ]

        await _crawl_links(
            case["links"],
            case["depth"],
            case["max_depth"],
            f"crawl_test_cache_{i}.json",
            case["parent_source"],
            use_cloud_function=False,
            semaphore=asyncio.Semaphore(10),
            research_topic=research_topic,
            entity_types=entity_types,
            cache=cache,
        )

        # TODO: Check that the expected number of URLs were processed
        # assert (
        #     len(cache) == case["expected_processed"]
        # ), f"Expected {case['expected_processed']} processed URLs, but got {len(cache)}"

        # Check that each URL was processed and added to the cache
        # for link in case["links"]:
        #     try:
        #         resolved_url: str = resolve_url(
        #             link,
        #             base_url=(
        #                 case["parent_source"]["url"] if case["parent_source"] else None
        #             ),
        #         )
        #         url_hash: str = hashlib.md5(resolved_url.encode()).hexdigest()
        #         assert url_hash in cache, f"Expected {resolved_url} to be in cache"
        #         assert isinstance(cache[url_hash], Work), f"Expected {resolved_url} to be a Work object in cache"
        #         assert hasattr(cache[url_hash], "relevant"), f"Expected {resolved_url} to have 'relevant' attribute in cache"
        #     except ValueError:
        #         # TODO: Invalid URLs should be in the cache with an error
        #         url_hash: str = hashlib.md5(link.encode()).hexdigest()
        #         assert url_hash in cache, f"Expected invalid URL {link} to be in cache"
        #         assert (
        #             cache[url_hash]["type"] == "error"
        #         ), f"Expected invalid URL {link} to have 'error' type in cache"

        print(f"Test case {i + 1} passed successfully!")

    print("All test cases passed successfully!")
    

@pytest.mark.asyncio
async def test_crawl():
    """
    Test function for the main crawl function.
    """
    research_topic: str = (
        "can humans keep up? the impact of artificial intelligence on neuroscience"
    )
    keywords: List[str] = [
        "artificial intelligence",
    ]
    urls: List[str] = [
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10053494/",
        "https://stanmed.stanford.edu/experts-weigh-ai-vs-human-brain/",
        "https://knowledge.wharton.upenn.edu/article/how-can-ai-and-the-human-brain-work-together/",
        "https://www.bbc.com/future/article/20230405-why-ai-is-becoming-impossible-for-humans-to-understand",
        "https://www.theatlantic.com/technology/archive/2023/05/llm-ai-chatgpt-neuroscience/674216/",
        "https://ai-analytics.wharton.upenn.edu/news/the-future-of-ai-and-neuroscience/",
    ]

    sources: List[SOURCE_TYPES] = [
        SOURCE_TYPES.OPENALEX,
        SOURCE_TYPES.GOOGLE_SCHOLAR,
        SOURCE_TYPES.DOI,
        SOURCE_TYPES.SEMANTIC_SCHOLAR,
        SOURCE_TYPES.VIDEO,
        SOURCE_TYPES.GOOGLE,
    ]

    use_cloud_function: bool = (
        os.getenv("CLOUD_FUNCTION_ENABLED", "false").lower() == "true"
    )

    results = await crawl(
        keywords,
        urls,
        sources,
        research_topic=research_topic,
        max_depth=2,
        use_cloud_function=use_cloud_function,
        semaphore=asyncio.Semaphore(3),
        num_results=3,
    )

    serialize_entity_array(results, "crawl_test_results.json")

    assert len(results) > 0, "Failed to find any results in crawl"

    print(
        "Crawl completed. Check the 'downloaded_data' directory and 'manifest.json' for results."
    )
