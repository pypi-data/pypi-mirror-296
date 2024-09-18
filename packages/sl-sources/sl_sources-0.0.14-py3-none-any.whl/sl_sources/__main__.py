# sl_sources/__main__.py

import argparse
import asyncio
import json

from sl_sources.doi import search_and_download_doi, search_doi, download_from_doi
from sl_sources.google_scholar import (
    search_and_download_from_google_scholar,
    search_google_scholar,
    download_from_google_scholar,
)
from sl_sources.google_books import (
    download_from_google_books,
    search_and_download_from_google_books,
    search_google_books,
)

from sl_sources.http import ThrottledClientSession
from sl_sources.models import SOURCE_TYPES, WORK_TYPES, SearchInput, Work
from sl_sources.openalex import (
    search_and_download_from_openalex,
    search_openalex,
    download_from_openalex,
)
from sl_sources.google import (
    search_and_download_from_google,
    search_google,
    download_from_google_search,
)
from sl_sources.podcasts import (
    download_podcast,
    search_and_download_podcasts,
    search_podcasts,
)
from sl_sources.semantic_scholar import (
    download_from_semantic_scholar,
    search_and_download_from_semantic_scholar,
    search_semantic_scholar,
)
from sl_sources.user_agent import get_user_agent_header
from sl_sources.video import (
    search_and_download_from_media_site,
    search_youtube,
    download_from_media_site,
)


async def main():
    parser = argparse.ArgumentParser(
        description="Search and download from various sources"
    )
    parser.add_argument(
        "action", choices=["search", "download", "crawl"], help="Action to perform"
    )
    parser.add_argument(
        "source",
        choices=[
            SOURCE_TYPES.GOOGLE_SCHOLAR,
            SOURCE_TYPES.OPENALEX,
            SOURCE_TYPES.DOI,
            SOURCE_TYPES.GOOGLE,
            SOURCE_TYPES.SEMANTIC_SCHOLAR,
            SOURCE_TYPES.VIDEO,
            SOURCE_TYPES.PODCAST,
        ],
        help="Source to search or download from",
    )
    parser.add_argument("query", help="Search query or ID")
    parser.add_argument(
        "--num_results",
        type=int,
        default=10,
        help="Number of results to return (for search)",
    )
    parser.add_argument("--output", help="Output file for results (optional)")

    args = parser.parse_args()

    if args.actions == "search_and_download":
        if args.source_type == SOURCE_TYPES.GOOGLE_SCHOLAR:
            results = await search_and_download_from_google_scholar(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.GOOGLE_BOOKS:
            results = await search_and_download_from_google_books(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.OPENALEX:
            results = await search_and_download_from_openalex(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.DOI:
            results = await search_and_download_doi(args.query, args.num_results)
        elif args.source_type == SOURCE_TYPES.GOOGLE:
            results = await search_and_download_from_google(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.SEMANTIC_SCHOLAR:
            results = await search_and_download_from_semantic_scholar(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        # elif args.source_type == SOURCE_TYPES.TWITTER:
        # results = await search_twitter(SearchInput(query=args.query, num_results=args.num_results))
        elif args.source_type == SOURCE_TYPES.VIDEO:
            results = await search_and_download_from_media_site(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.PODCAST:
            results = await search_and_download_podcasts(
                SearchInput(query=args.query, num_results=args.num_results)
            )

    if args.action == "search":
        if args.source_type == SOURCE_TYPES.GOOGLE_SCHOLAR:
            results = await search_google_scholar(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.GOOGLE_BOOKS:
            results = await search_google_books(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.OPENALEX:
            results = await search_openalex(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.DOI:
            results = await search_doi(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.GOOGLE:
            results = await search_google(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.SEMANTIC_SCHOLAR:
            results = await search_semantic_scholar(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        # elif args.source_type == SOURCE_TYPES.TWITTER:
        #     results = await search_twitter(SearchInput(query=args.query, num_results=args.num_results))
        elif args.source_type == SOURCE_TYPES.VIDEO:
            results = await search_youtube(
                SearchInput(query=args.query, num_results=args.num_results)
            )
        elif args.source_type == SOURCE_TYPES.PODCAST:
            results = await search_podcasts(
                SearchInput(query=args.query, num_results=args.num_results)
            )

    elif args.action == "download":
        async with ThrottledClientSession(
            rate_limit=15 / 60, headers=get_user_agent_header()
        ) as session:
            work = Work(**args.search_result)

            if args.source_type == SOURCE_TYPES.GOOGLE_SCHOLAR:
                if work.work_type == WORK_TYPES.UNKNOWN:
                    work.work_type = WORK_TYPES.PAPER
                results = await download_from_google_scholar(work, session)
            elif args.source_type == SOURCE_TYPES.GOOGLE_BOOKS:
                if work.work_type == WORK_TYPES.UNKNOWN:
                    work.work_type = WORK_TYPES.BOOK
                results = await download_from_google_books(work, session)
            elif args.source_type == SOURCE_TYPES.OPENALEX:
                if work.work_type == WORK_TYPES.UNKNOWN:
                    work.work_type = WORK_TYPES.PAPER
                results = await download_from_openalex(work, session)
            elif args.source_type == SOURCE_TYPES.DOI:
                if work.work_type == WORK_TYPES.UNKNOWN:
                    work.work_type = WORK_TYPES.PAPER
                results = await download_from_doi(work)
            elif args.source_type == SOURCE_TYPES.GOOGLE:
                results = await download_from_google_search(work)
            elif args.source_type == SOURCE_TYPES.SEMANTIC_SCHOLAR:
                if work.work_type == WORK_TYPES.UNKNOWN:
                    work.work_type = WORK_TYPES.PAPER
                results = await download_from_semantic_scholar(work, session)
            # elif args.source_type == SOURCE_TYPES.TWITTER:
            #     results = await download_twitter({"tweet_id": args.query})
            elif args.source_type == SOURCE_TYPES.VIDEO:
                if work.work_type == WORK_TYPES.UNKNOWN:
                    work.work_type = WORK_TYPES.VIDEO
                results = await download_from_media_site(work)
            elif args.source_type == SOURCE_TYPES.PODCAST:
                results = await download_podcast(work)
            else:
                print(f"Download not supported for {args.source_type}")
                return

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
