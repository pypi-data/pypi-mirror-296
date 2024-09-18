# Society Library Sources

`sl_sources` is a powerful and flexible Python library designed to streamline the process of collecting and processing data from various online sources. It provides a unified interface for searching, downloading, and managing content from multiple platforms, making it an essential tool for researchers, data scientists, and developers working with diverse data sources.

Whether you're conducting academic research, performing data analysis, or building applications that require access to a wide range of information, `sl_sources` offers a comprehensive solution to simplify your data collection workflow.

## Key Features

- **Multi-Source Support**: Seamlessly search and download from a variety of sources including Google Scholar, OpenAlex, DOI (Digital Object Identifier), Google, Semantic Scholar, YouTube, and more. This feature allows you to access a wide range of academic and general information from a single interface.

- **Flexible Search Options**: Perform targeted searches with customizable parameters. You can specify the number of results, entity types (e.g., works, authors, institutions), and source-specific options to fine-tune your queries.

- **Efficient Data Retrieval**: Download full-text content and metadata from search results. The library handles the complexities of accessing and parsing different data formats, providing you with clean, structured data.

- **Scalable Architecture**: Designed for easy integration with worker-based pipelines for large-scale data collection. This allows you to distribute your workload across multiple machines or processes, enabling efficient processing of large datasets.

- **Pydantic Models**: Utilize strongly-typed data models for consistent and reliable data handling. This ensures that the data you work with is well-structured and validates against a predefined schema, reducing errors and improving code reliability.

- **Crawling Capabilities**: Explore interconnected content by crawling links and following trails of related information. This is particularly useful for building comprehensive datasets or understanding the structure of information in a particular domain.

- **CAPTCHA Solving Integration**: Built-in support for CAPTCHA solving services to handle protected content, ensuring smoother data collection from sources that employ anti-bot measures.

## Installation

Install `sl_sources` using pip, the Python package installer. Open your terminal or command prompt and run:

```bash
pip install sl_sources
```

This command will download and install the latest version of `sl_sources` along with its dependencies.

## Basic Usage

Here's a basic example of how to use `sl_sources` for searching and downloading content:

```python
from sl_sources import search_source, download_search_result, search_and_download
from sl_sources.models import SearchInput, ENTITY_TYPES, SOURCE_TYPES

async def basic_usage_example():
    # Perform a search
    search_results = await search_source(
        SearchInput(
            query="artificial intelligence",  # The search query
            num_results=5,  # Number of results to return
            source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,  # The source to search
            entity_types=[ENTITY_TYPES.WORK, ENTITY_TYPES.AUTHOR]  # Types of entities to retrieve
        )
    )

    # Download a specific result
    for result in search_results:
        full_content = await download_search_result(result)
        print(f"Downloaded content for {result.name}: {full_content[:100]}...")  # Print first 100 characters

    # Search and download in one step
    combined_results = await search_and_download(
        SearchInput(
            query="machine learning",
            num_results=3,
            source_type=SOURCE_TYPES.OPENALEX,
            entity_types=[ENTITY_TYPES.WORK]
        )
    )
    
    for result in combined_results:
        print(f"Combined search and download result: {result.name}")

# Run the async function
import asyncio
asyncio.run(basic_usage_example())
```

In this example:
1. We first perform a search using `search_source`, which returns a list of search results.
2. We then iterate through these results and download the full content for each using `download_search_result`.
3. Finally, we demonstrate the `search_and_download` function, which combines the search and download steps into a single operation.

This basic usage shows the core functionality of `sl_sources`, allowing you to quickly search and retrieve content from various sources.

## Source-Specific Usage

Different sources may have unique features or requirements. Here are examples of how to use `sl_sources` with specific sources:

### OpenAlex: Searching for Neuroscience Authors

```python
from sl_sources import search_and_download_from_openalex
from sl_sources.models import SearchInput, ENTITY_TYPES, SOURCE_TYPES

async def openalex_author_search():
    # Use case: Find top authors in neuroscience field
    results = await search_and_download_from_openalex(
        SearchInput(
            query="neuroscience",  # Search term
            num_results=10,  # Number of results to fetch
            entity_types=[ENTITY_TYPES.AUTHOR],  # Only search for authors
            source_type=SOURCE_TYPES.OPENALEX  # Specify OpenAlex as the source
        )
    )
    for author in results:
        print(f"Author: {author.name}, Works: {len(author.works)}")
        # You can further process author information here

asyncio.run(openalex_author_search())
```

In this example, we're using OpenAlex to find top authors in the field of neuroscience. This can be useful for identifying key researchers in a specific domain, which could be valuable for literature reviews, collaboration opportunities, or understanding the landscape of a particular field of study.

### Google Scholar: AI Works, Authors, and Publishers

```python
from sl_sources import search_and_download_from_google_scholar
from sl_sources.models import SearchInput, ENTITY_TYPES, SOURCE_TYPES, Work, Author, Publisher

async def google_scholar_ai_search():
    # Use case: Comprehensive search for AI research
    results = await search_and_download_from_google_scholar(
        SearchInput(
            query="artificial intelligence",  # Search term
            num_results=5,  # Number of results to fetch
            entity_types=[ENTITY_TYPES.WORK, ENTITY_TYPES.AUTHOR, ENTITY_TYPES.PUBLISHER],  # Search for works, authors, and publishers
            source_type=SOURCE_TYPES.GOOGLE_SCHOLAR  # Specify Google Scholar as the source
        )
    )
    for entity in results:
        if isinstance(entity, Work):
            print(f"Work: {entity.name}")
            print(f"  Authors: {', '.join(a.name for a in entity.authors)}")
            print(f"  Abstract: {entity.abstract[:100]}...")  # Print first 100 characters of abstract
        elif isinstance(entity, Author):
            print(f"Author: {entity.name}")
            print(f"  Affiliations: {', '.join(str(i) for i in entity.institutions)}")
        elif isinstance(entity, Publisher):
            print(f"Publisher: {entity.name}")
        print("---")

asyncio.run(google_scholar_ai_search())
```

This example demonstrates a more comprehensive search using Google Scholar, targeting works, authors, and publishers related to artificial intelligence. This type of search is beneficial when you want to get a broad overview of a field, including not just the research papers, but also key authors and publishing venues.

## Multi-threading and Distributed Workload

For large-scale data collection, you can use asyncio to distribute the workload across multiple threads or processes. This is particularly useful when you need to collect a large amount of data quickly, or when you're working with rate-limited APIs and want to maximize your throughput.

Here's an example of how to implement this:

```python
import asyncio
from sl_sources import search_source, download_search_result
from sl_sources.models import SearchInput, ENTITY_TYPES, SOURCE_TYPES

async def search_and_download_batch(query, source_type, start, batch_size):
    search_results = await search_source(
        SearchInput(
            query=query,
            num_results=batch_size,
            source_type=source_type,
            entity_types=[ENTITY_TYPES.WORK]
        )
    )
    
    download_tasks = [download_search_result(result) for result in search_results]
    return await asyncio.gather(*download_tasks)

async def main():
    query = "artificial intelligence"
    source_type = SOURCE_TYPES.GOOGLE_SCHOLAR
    total_results = 100
    batch_size = 10

    tasks = [
        search_and_download_batch(query, source_type, i, batch_size)
        for i in range(0, total_results, batch_size)
    ]
    
    all_results = await asyncio.gather(*tasks)
    flattened_results = [item for sublist in all_results for item in sublist]
    
    print(f"Total downloaded results: {len(flattened_results)}")
    # Further process or analyze the results here

asyncio.run(main())
```

In this example:
1. We define a `search_and_download_batch` function that performs a search and downloads the results for a specific batch.
2. In the `main` function, we create multiple tasks, each handling a batch of results.
3. We use `asyncio.gather` to run all these tasks concurrently.
4. Finally, we flatten the results and can proceed with further processing or analysis.

This approach allows you to efficiently collect large amounts of data by parallelizing the work. It's particularly useful when dealing with large datasets or when you need to respect rate limits imposed by the data sources.

## Crawling

The `sl_sources` library also supports crawling, which is useful for exploring interconnected content or following a trail of related information. Crawling can be particularly valuable when you want to build a comprehensive dataset around a topic or understand the structure of information in a particular domain.

### Why Crawl vs. Search and Download?

- **Crawling**:
  - Useful for exploring a network of related content
  - Allows following links between documents
  - Helps in discovering new, potentially relevant sources
  - Ideal for building a comprehensive dataset around a topic
  - Helps in understanding the structure of information in a domain

- **Search and Download**:
  - Better for targeted data collection
  - More efficient when you know exactly what you're looking for
  - Useful for gathering specific information without exploring related content
  - Typically faster when you need a well-defined set of data

### Crawling Example

Here's an example of how to use the crawling functionality:

```python
from sl_sources.crawl import crawl
from sl_sources.models import CrawlInput, ENTITY_TYPES

async def crawling_example():
    research_topic = "Impact of AI on climate change research"
    keywords = ["artificial intelligence", "climate change", "machine learning"]
    urls = [
        "https://www.example.com/ai-climate-research",
        "https://www.example.org/machine-learning-environment"
    ]

    await crawl(
        CrawlInput(
            keywords=keywords,
            urls=urls,
            sources=["openalex", "google_scholar"],
            research_topic=research_topic,
            max_depth=2,  # How many levels deep to crawl
            use_cloud_function=False,
            entity_types=[ENTITY_TYPES.WORK, ENTITY_TYPES.AUTHOR]
        )
    )
    
    # The results will be saved to files in the current directory
    print("Crawling completed. Check the output files for results.")

asyncio.run(crawling_example())
```

In this example:
1. We define a research topic and a list of keywords related to it.
2. We provide some starting URLs for the crawler.
3. We specify which sources to use for additional searches (OpenAlex and Google Scholar in this case).
4. We set a maximum depth for the crawler to explore.
5. We specify which types of entities we're interested in (works and authors).

The crawler will start from the given URLs, search for the keywords, and follow links to related content, up to the specified depth. It will also use the specified sources to find additional relevant content.

### Crawling Links Only

If you want to crawl only the links without using keywords, you can do so by leaving the `keywords` list empty:

```python
await crawl(
    CrawlInput(
        keywords=[],
        urls=["https://www.example.com/start-page"],
        sources=[],
        max_depth=3,
        use_cloud_function=False,
        entity_types=[ENTITY_TYPES.WORK]
    )
)
```

This approach is useful when you want to explore the structure of a website or a network of related pages, without being guided by specific search terms.

### Crawling Keywords Only

Conversely, if you want to search for keywords without starting from specific URLs, you can do so by leaving the `urls` list empty:

```python
await crawl(
    CrawlInput(
        keywords=["artificial intelligence", "machine learning"],
        urls=[],
        sources=["google_scholar", "openalex"],
        max_depth=2,
        use_cloud_function=False,
        entity_types=[ENTITY_TYPES.WORK, ENTITY_TYPES.AUTHOR]
    )
)
```

This method is beneficial when you're interested in collecting all available information on specific topics across multiple sources, without being constrained to a particular starting point.

### Crawling YouTube Links

Here's an example of how to crawl YouTube links, which can be useful for collecting information from video content:

```python
from sl_sources.crawl import crawl
from sl_sources.models import Work, Author, CrawlInput, ENTITY_TYPES

async def crawl_youtube_example():
    research_topic = "Can humans keep up? The impact of artificial intelligence on neuroscience and the future of human intelligence"
    
    # Example YouTube links
    youtube_links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=ZNGiDDk1jOY",
        "https://www.youtube.com/watch?v=8XqYgSkCHCE"
    ]

    works = [
        Work(
            id=url.split('=')[1],
            name=f"YouTube Video {i+1}",
            url=url,
            abstract="",
            full_text='',
            authors=[Author(name="Unknown", source_type="youtube")],
            source_type="youtube",
            year=None
        ) for i, url in enumerate(youtube_links)
    ]

    await crawl(
        CrawlInput(
            keywords=[],
            urls=[work.url for work in works],
            sources=[],
            research_topic=research_topic,
            max_depth=0,
            use_cloud_function=False,
            entity_types=[ENTITY_TYPES.WORK, ENTITY_TYPES.AUTHOR]
        )
    )
    
    print("YouTube crawling completed. Check the output files for results.")

asyncio.run(crawl_youtube_example())
```

This example demonstrates how to crawl specific YouTube videos. It's particularly useful when you want to analyze video content related to your research topic. The crawler will attempt to extract information such as the video title, description, and potentially the transcript if available.

## Cloud Function Worker Setup

For large-scale data collection tasks, it's often beneficial to offload the work to cloud functions. This allows for better scalability and can help manage rate limits and resource usage more effectively. Here's how to set up and use a Cloud Function worker with `sl_sources`:

### Prerequisites

1. A Google Cloud account with billing enabled
2. Google Cloud SDK (gcloud) installed on your local machine
3. Python 3.7 or later installed

### Setup Steps

1. **Create a Google Cloud Project**

   If you haven't already, create a new project in the Google Cloud Console.

2. **Enable Required APIs**

   Enable the following APIs for your project:
   - Cloud Functions API
   - Cloud Build API

   You can do this through the Google Cloud Console or use the following gcloud commands:

   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

3. **Install and Initialize gcloud CLI**

   If you haven't already, download and install the gcloud CLI, then initialize it:

   ```bash
   gcloud init
   gcloud auth login
   ```

4. **Prepare Your Environment**

   Create a `.env` file in your project root with the necessary API keys and settings:

   ```
   GOOGLE_API_KEY=your_google_api_key
   SEMANTIC_SCHOLAR_API_KEY=your_semantic_scholar_api_key
   CAPSOLVER_API_KEY=your_capsolver_api_key
   CLOUD_FUNCTION_ENABLED=true
   CLOUD_FUNCTION_URL=https://your-region-your-project.cloudfunctions.net/media_worker
   ```

### Deploying the Worker

1. **Create a `requirements.txt` file**

   Ensure all necessary dependencies are listed.

2. **Create a `main.py` file**

   This will contain your Cloud Function code. Here's a basic example:

   ```python
   from sl_sources import search_source, download_search_result
   from sl_sources.models import SearchInput

   def handle_request(request):
       data = request.get_json()
       if data['request_type'] == 'search':
           return search_source(SearchInput(**data))
       elif data['request_type'] == 'download':
           return download_search_result(data['search_result'])
   ```

3. **Deploy the Function**

   Use the following gcloud command to deploy:

   ```bash
   gcloud functions deploy media_worker \
       --runtime python39 \
       --trigger-http \
       --allow-unauthenticated
   ```

   Note the URL provided in the deployment output. Update your `.env` file with this URL.


## CAPTCHA Solving

`sl_sources` includes built-in support for CAPTCHA solving, which can be crucial when dealing with sources that employ anti-bot measures. To enable CAPTCHA solving:

1. Sign up for a CAPTCHA solving service (e.g., Capsolver).
2. Get your API key from the service.
3. Set the API key in your environment:

   ```bash
   export CAPSOLVER_API_KEY=your_capsolver_api_key
   ```

   Or add it to your `.env` file:

   ```
   CAPSOLVER_API_KEY=your_capsolver_api_key
   ```

The library will automatically use this service when it encounters a CAPTCHA.

### Using the Cloud Function Worker

To use the deployed worker in your code:

```python
import os
from sl_sources.http import cloud_function_request
from sl_sources.models import SearchInput, SOURCE_TYPES, ENTITY_TYPES

async def use_cloud_worker():
    search_input = SearchInput(
        query="artificial intelligence",
        num_results=5,
        source_type=SOURCE_TYPES.GOOGLE_SCHOLAR,
        entity_types=[ENTITY_TYPES.WORK]
    )
    
    results = await cloud_function_request("search", search_input.dict())
    
    for result in results:
        full_content = await cloud_function_request("download", {"search_result": result})
        print(f"Downloaded content for {result['name']}: {full_content[:100]}...")

# Run the async function
import asyncio
asyncio.run(use_cloud_worker())
```

This setup allows you to offload resource-intensive tasks to the cloud, enabling better scalability for large data collection projects.

## Publishing to PyPI

If you've made improvements to `sl_sources` or are maintaining your own fork, you might want to publish it to PyPI. Here's how to do that:

1. **Prepare Your Project**

   Ensure your project structure is correct and you have a `setup.py` file.

2. **Update Version Number**

   In your `setup.py` or `__init__.py`, update the version number.

3. **Create Distribution Files**

   ```bash
   python setup.py sdist bdist_wheel
   ```

4. **Upload to PyPI**

   First, install twine if you haven't:
   ```bash
   pip install twine
   ```

   Then, upload your distribution:
   ```bash
   twine upload dist/*
   ```

   You'll be prompted for your PyPI credentials.

5. **Verify the Upload**

   Check your package page on PyPI to ensure everything looks correct.

Alternatively, you can use this one-liner to build and upload:

```bash
rm -rf dist && python setup.py sdist bdist_wheel && twine upload dist/*
```

Remember to increment your version number each time you publish an update.