from sl_sources.podcasts import download_podcast, search_podcasts

from .doi import download_from_doi, search_and_download_doi, search_doi
from .google import (download_from_google_search,
                     search_and_download_from_google, search_google)
from .google_books import (download_from_google_books,
                           search_and_download_from_google_books,
                           search_google_books)
from .google_scholar import (download_from_google_scholar,
                             search_and_download_from_google_scholar,
                             search_google_scholar)
from .http import ThrottledClientSession
from .models import SOURCE_TYPES, SearchInput
from .openalex import (download_from_openalex,
                       search_and_download_from_openalex, search_openalex)
from .semantic_scholar import (download_from_semantic_scholar,
                               search_and_download_from_semantic_scholar,
                               search_semantic_scholar)
from .user_agent import get_user_agent_header
# from .twitter import search_twitter  # Twitter search is currently not implemented
from .video import (download_from_media_site,
                    search_and_download_from_media_site, search_youtube)


async def search_and_download(search_input: SearchInput):
    """
    Perform a search and download operation based on the provided search input.

    This function acts as a router, directing the search and download request to the
    appropriate source-specific function. This design allows for easy addition of new
    sources and keeps the main logic clean and maintainable.

    Parameters:
    -----------
    search_input : SearchInput
        An object containing all necessary parameters for the search, including
        the source type, query, number of results, and entity types.

    Returns:
    --------
    List
        A list of search results, with each result downloaded and processed.
    """
    # Route the request based on the source type
    if search_input.source_type == SOURCE_TYPES.OPENALEX:
        print("Searching and downloading from OpenAlex")
        results = await search_and_download_from_openalex(search_input)
    elif search_input.source_type == SOURCE_TYPES.GOOGLE_SCHOLAR:
        print("Searching and downloading from Google Scholar")
        results = await search_and_download_from_google_scholar(search_input)
    elif search_input.source_type == SOURCE_TYPES.GOOGLE_BOOKS:
        print("Searching and downloading from Google Books")
        results = await search_and_download_from_google_books(search_input)
    elif search_input.source_type == SOURCE_TYPES.SEMANTIC_SCHOLAR:
        print("Searching and downloading from Semantic Scholar")
        results = await search_and_download_from_semantic_scholar(search_input)
    elif search_input.source_type == SOURCE_TYPES.DOI:
        print("Searching and downloading from DOI")
        results = await search_and_download_doi(search_input)
    elif search_input.source_type == SOURCE_TYPES.GOOGLE:
        print("Searching and downloading from Google")
        results = await search_and_download_from_google(search_input)
    elif search_input.source_type == SOURCE_TYPES.VIDEO:
        print("Searching and downloading from Youtube")
        results = await search_and_download_from_media_site(search_input)
    else:
        raise ValueError(f"Unrecognized source type: {search_input.source_type}")

    print(
        f"Found and downloaded {len(results)} results from {search_input.source_type}"
    )
    return results


async def search_source(search_input: SearchInput):
    """
    Perform a search operation on a specific source.

    This function is used when we need to separate the search and download steps,
    or when dealing with a source type that isn't explicitly handled in search_and_download.

    Parameters:
    -----------
    search_input : SearchInput
        An object containing all necessary parameters for the search.

    Returns:
    --------
    List
        A list of search results (not downloaded).
    """
    source = search_input.source_type
    query = search_input.query
    num_results = search_input.num_results
    entity_types = search_input.entity_types

    # Route the search request based on the source type
    if source == SOURCE_TYPES.GOOGLE or source == SOURCE_TYPES.CRAWL:
        print("Searching Google")
        results = await search_google(
            SearchInput(query=query, num_results=num_results, entity_types=entity_types)
        )
        for result in results:
            if "semanticscholar.org" in result.url:
                result.source_type = SOURCE_TYPES.SEMANTIC_SCHOLAR
    elif source == SOURCE_TYPES.SEMANTIC_SCHOLAR:
        print("Searching Semantic Scholar")
        results = await search_semantic_scholar(
            SearchInput(query=query, num_results=num_results, entity_types=entity_types)
        )
    elif source == SOURCE_TYPES.GOOGLE_SCHOLAR:
        print("Searching Google Scholar")
        results = await search_google_scholar(
            SearchInput(query=query, num_results=num_results, entity_types=entity_types)
        )
        for result in results:
            if "semanticscholar.org" in result.url:
                result.source_type = SOURCE_TYPES.SEMANTIC_SCHOLAR
    elif source == SOURCE_TYPES.GOOGLE_BOOKS:
        print("Searching Google Books")
        results = await search_google_books(
            SearchInput(query=query, num_results=num_results, entity_types=entity_types)
        )
    elif source == SOURCE_TYPES.OPENALEX:
        print("Searching OpenAlex")
        results = await search_openalex(
            SearchInput(query=query, num_results=num_results, entity_types=entity_types)
        )
    elif source == SOURCE_TYPES.DOI:
        print("Searching DOI")
        results = await search_doi(
            SearchInput(query=query, num_results=num_results, entity_types=entity_types)
        )
    elif source == SOURCE_TYPES.VIDEO:
        print("Searching Youtube")
        results = await search_youtube(
            SearchInput(query=query, num_results=num_results, entity_types=entity_types)
        )
    elif source == SOURCE_TYPES.PODCAST:
        print("Searching Podcasts")
        results = await search_podcasts(
            SearchInput(query=query, num_results=num_results, entity_types=entity_types)
        )
    else:
        # If an unrecognized source is provided, we return an empty list
        # This allows the program to continue running even if an invalid source is given
        print(f"Unrecognized source: {source}")
        return []

    print(f"Found {len(results)} results from {source}")
    return results


async def download_search_result(search_result):
    """
    Download the full content for a single search result.

    This function is used to fetch the complete information for a search result,
    which may include the full text of an article, video transcripts, etc.

    Parameters:
    -----------
    search_result : Any
        A single search result object. The exact type depends on the source.

    Returns:
    --------
    Any
        The search result with additional downloaded information.
    """
    print(f"Downloading {search_result.url}")
    source_type = search_result.source_type

    if "semanticscholar.org" in search_result.url:
        source_type = SOURCE_TYPES.SEMANTIC_SCHOLAR

    async with ThrottledClientSession(
        rate_limit=15 / 60, headers=get_user_agent_header()
    ) as session:
        # Route the download request based on the source type
        if source_type in [SOURCE_TYPES.CRAWL, SOURCE_TYPES.GOOGLE]:
            # For both crawl and google, we use the same download function
            print("Downloading search result from google")
            result = await download_from_google_search(search_result)
        elif source_type == SOURCE_TYPES.TWITTER:
            # For Twitter, we currently just return the search result as-is
            # This might be changed in the future if we implement Twitter-specific downloading
            result = search_result
            result = await download_from_media_site(search_result)
        elif source_type == SOURCE_TYPES.GOOGLE_SCHOLAR:
            print("Downloading search result from google scholar")
            result = await download_from_google_scholar(search_result, session)
        elif source_type == SOURCE_TYPES.SEMANTIC_SCHOLAR:
            print("Downloading search result from semantic scholar")
            result = await download_from_semantic_scholar(search_result, session)
        elif source_type == SOURCE_TYPES.GOOGLE_BOOKS:
            print("Downloading search result from google books")
            result = await download_from_google_books(search_result, session)
        elif source_type == SOURCE_TYPES.OPENALEX:
            print("Downloading search result from openalex")
            result = await download_from_openalex(search_result, session)
        elif source_type == SOURCE_TYPES.DOI:
            print("Downloading search result from doi")
            result = await download_from_doi(search_result)
        elif source_type == SOURCE_TYPES.VIDEO:
            print("Downloading search result from youtube")
        elif source_type == SOURCE_TYPES.PODCAST:
            print("Downloading search result from podcast")
            result = await download_podcast(search_result)
        else:
            # If we don't have a specific download function for this source type,
            # we return the search result as-is
            print(f"Unrecognized source type: {source_type}")
            result = search_result

        return result