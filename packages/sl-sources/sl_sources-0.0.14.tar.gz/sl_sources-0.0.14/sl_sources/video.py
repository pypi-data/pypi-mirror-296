import asyncio
import glob
import hashlib
import json
import logging
import os
import re
import tempfile
from multiprocessing import Pool
from typing import Any, Dict, List, Optional
from uuid import uuid4

import urllib
import requests
import yt_dlp
from yt_dlp import YoutubeDL

from .audio_transcriber import transcribe
from .models import SOURCE_TYPES, WORK_TYPES, Author, SearchInput, Work

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def can_download_with_ytdlp(url: str) -> bool:
    """
    Check if a URL can be downloaded with yt-dlp.

    Parameters
    ----------
    url : str
        The URL to check.

    Returns
    -------
    bool
        True if the URL can be downloaded with yt-dlp, False otherwise.
    """
    extractors = yt_dlp.extractor.gen_extractors()
    for extractor in extractors:
        if extractor.suitable(url) and extractor.IE_NAME != "generic":
            return True
    return False

def extract_video_id(url: str) -> str:
    """
    Extract the video ID from various video platform URLs.

    Parameters
    ----------
    url : str
        The URL of the video.

    Returns
    -------
    str
        The extracted video ID or a hash of the URL if extraction fails.
    """
    youtube_patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:embed\/|v\/|youtu.be\/)([0-9A-Za-z_-]{11})",
    ]
    vimeo_pattern = r"(?:vimeo\.com\/|video\/)(\d+)"
    dailymotion_pattern = r"(?:dailymotion\.com\/video\/)([a-zA-Z0-9]+)"

    for pattern in youtube_patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    match = re.search(vimeo_pattern, url)
    if match:
        return match.group(1)

    match = re.search(dailymotion_pattern, url)
    if match:
        return match.group(1)

    return hashlib.md5(url.encode()).hexdigest()


def get_video_metadata(url: str) -> Dict[str, Any]:
    """
    Get metadata for a video using yt-dlp.

    Parameters
    ----------
    url : str
        The URL of the video.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the video metadata.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return {
                "id": info.get("id", ydl.prepare_filename(info)),
                "title": info.get("title", "Unknown Title"),
                "description": info.get("description", ""),
                "duration": info.get("duration", 0),
                "upload_date": info.get("upload_date", ""),
                "year": info.get("release_year") or info.get("upload_date", "")[:4],
                "uploader": info.get("uploader", "Unknown Uploader"),
                "uploader_id": info.get("uploader_id", ""),
                "uploader_url": info.get("uploader_url", ""),
                "channel_id": info.get("channel_id", ""),
                "channel_url": info.get("channel_url", ""),
                "view_count": info.get("view_count", 0),
                "like_count": info.get("like_count", 0),
                "thumbnail": info.get("thumbnail", ""),
                "webpage_url": info.get("webpage_url", url),
                "categories": info.get("categories", []),
                "tags": info.get("tags", []),
            }
        except Exception as e:
            logger.error(f"Error extracting metadata for {url}: {str(e)}")
            return {
                "id": ydl.prepare_filename({"url": url}),
                "title": "Unknown Title",
                "description": "",
                "duration": 0,
                "upload_date": "",
                "year": "",
                "uploader": "Unknown Uploader",
                "uploader_id": "",
                "uploader_url": "",
                "channel_id": "",
                "channel_url": "",
                "view_count": 0,
                "like_count": 0,
                "thumbnail": "",
                "webpage_url": url,
                "categories": [],
                "tags": [],
            }


def search_by_url(url: str) -> Work:
    """
    Create a Work object for a video URL.

    Parameters
    ----------
    url : str
        The URL of the video.

    Returns
    -------
    Work
        A Work object containing information about the video.
    """
    metadata = get_video_metadata(url)
    return Work(
        id=metadata["id"],
        name=metadata["title"],
        work_type=WORK_TYPES.VIDEO,
        url=metadata["webpage_url"],
        duration=str(metadata["duration"]),
        abstract=metadata["description"],
        source_type=SOURCE_TYPES.VIDEO,
        authors=[Author(name=metadata["uploader"], source_type=SOURCE_TYPES.VIDEO)],
        year=metadata["year"],
        view_count=metadata["view_count"],
        like_count=metadata["like_count"],
        thumbnail=metadata["thumbnail"],
        uploader_id=metadata["uploader_id"],
        uploader_url=metadata["uploader_url"],
        channel_id=metadata["channel_id"],
        channel_url=metadata["channel_url"],
        categories=metadata["categories"],
        tags=metadata["tags"],
    )


def _prepare_data(response: str) -> List[Dict[str, Any]]:
    """
    Extract and prepare the search data from the YouTube response.

    Parameters
    ----------
    response : str
        The HTML response from YouTube.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries containing the search results data.
    """
    start = response.index("ytInitialData") + len("ytInitialData") + 3
    end = response.index("};", start) + 1
    json_str = response[start:end]
    data = json.loads(json_str)
    searched_obj = data["contents"]["twoColumnSearchResultsRenderer"][
        "primaryContents"
    ]["sectionListRenderer"]["contents"]

    return searched_obj


def fetch_youtube_data(url: str) -> str:
    """
    Fetch HTML data from a YouTube URL.

    Parameters
    ----------
    url : str
        The YouTube URL to fetch data from.

    Returns
    -------
    str
        The HTML content of the YouTube page.

    Raises
    ------
    requests.RequestException
        If there's an error fetching data from YouTube.
    """
    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except requests.RequestException:
        raise requests.RequestException("Failed to fetch data from YouTube.")
    return response.text



def search_by_term(term: str, max_results: Optional[int] = None) -> List[Work]:
    """
    Search YouTube for videos based on a search term.

    Parameters
    ----------
    term : str
        The search term to use.
    max_results : Optional[int], optional
        The maximum number of results to return. If None, returns all results.

    Returns
    -------
    List[Work]
        A list of Work objects representing the search results.
    """
    encoded_search = urllib.parse.quote_plus(term)
    BASE_URL = "https://youtube.com"
    url = f"{BASE_URL}/results?search_query={encoded_search}&sp=CAM"
    response = fetch_youtube_data(url)

    results = []
    searched_obj = _prepare_data(response)

    for contents in searched_obj:
        for video in contents["itemSectionRenderer"]["contents"]:
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})

                # Extract the year from the publishedTimeText
                published_time_text = video_data.get("publishedTimeText", {}).get(
                    "simpleText", ""
                )
                year_match = re.search(r"\b(\d{4})\b", published_time_text)
                year = int(year_match.group(1)) if year_match else None

                abstract = (
                    video_data.get("descriptionSnippet", {})
                    .get("runs", [{}])[0]
                    .get("text", "")
                )
                if not abstract:
                    abstract = (
                        video_data.get("detailedMetadataSnippets", [{}])[0]
                        .get("snippetText", {})
                        .get("runs", [{}])[0]
                        .get("text", "")
                    )

                work = Work(
                    id=video_data.get("videoId", str(uuid4())),
                    name=video_data.get("title", {}).get("runs", [[{}]])[0].get("text"),
                    work_type=WORK_TYPES.VIDEO,
                    abstract=abstract,
                    url=f"{BASE_URL}{video_data.get('navigationEndpoint', {}).get('commandMetadata', {}).get('webCommandMetadata', {}).get('url')}",
                    duration=video_data.get("lengthText", {}).get("simpleText", "0"),
                    authors=[
                        Author(
                            name=video_data.get("longBylineText", {})
                            .get("runs", [[{}]])[0]
                            .get("text"),
                            source_type=SOURCE_TYPES.VIDEO,
                        )
                    ],
                    year=year,
                    source_type=SOURCE_TYPES.VIDEO,
                )
                results.append(work)

        if results:
            if max_results is not None and len(results) > max_results:
                return results[:max_results]

        break

    return results


async def search_youtube(search_input: SearchInput) -> List[Work]:
    """
    Asynchronous function to search YouTube based on the provided search input.

    Parameters
    ----------
    search_input : SearchInput
        The search input containing the query and number of results.

    Returns
    -------
    List[Work]
        A list of Work objects representing the search results.
    """
    query = search_input.query
    num_results = search_input.num_results
    search_results = search_by_term(query, max_results=num_results)
    return search_results


def download_video(url: str, temp_dir: str) -> str:
    """
    Download a video's audio using yt-dlp.

    Parameters
    ----------
    url : str
        The URL of the video.
    temp_dir : str
        The temporary directory to save the downloaded audio.

    Returns
    -------
    str
        The path to the downloaded audio file.
    """
    ydl_opts = {
        "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(temp_dir, f"{info['id']}.mp3")


def vtt_to_text(vtt_data: str) -> str:
    """
    Convert VTT subtitle data to plain text.

    Parameters
    ----------
    vtt_data : str
        The VTT subtitle data as a string.

    Returns
    -------
    str
        The extracted text from the VTT data.
    """
    lines = vtt_data.strip().split("\n")
    transcript = []

    for line in lines:
        if (
            not re.match(r"\d{2}:\d{2}:\d{2}\.\d{3}", line)
            and not line.strip().isdigit()
        ):
            transcript.append(line.strip())

    return " ".join(transcript)


def download_with_ytdl(work: Work) -> Work:
    """
    Synchronous function to download and process a video.

    This function attempts to download subtitles if available, otherwise
    it downloads the audio and transcribes it.

    Parameters
    ----------
    work : Work
        The Work object representing the video.

    Returns
    -------
    Work
        The updated Work object with the full text (transcript) added.
    """
    logger.info(f"Downloading video: {work.url}")

    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            "writesubtitles": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(work.url, download=True)
                video_id = info.get("id", ydl.prepare_filename(info))
            except Exception as e:
                logger.error(
                    f"Error downloading video or subtitles for {work.url}: {str(e)}"
                )
                video_id = ydl.prepare_filename({"url": work.url})

        vtt_files = glob.glob(os.path.join(temp_dir, f"{video_id}.*.vtt"))
        if vtt_files:
            vtt_file = vtt_files[0]
            try:
                with open(vtt_file, "r", encoding="utf-8") as f:
                    vtt_data = f.read()
                transcript = vtt_to_text(vtt_data)
                work.full_text = transcript
                return work
            except Exception as e:
                logger.error(f"Error reading VTT file: {e}")

        logger.info(
            "No VTT file found or error occurred, attempting to transcribe audio with Whisper"
        )
        try:
            audio_file = download_video(work.url, temp_dir)
            if os.path.exists(audio_file):
                work.full_text = transcribe(audio_file)
                return work
            else:
                logger.error(f"Error: Audio file {audio_file} not found.")
                return work
        except Exception as e:
            logger.error(f"Error in audio transcription: {e}")
            return work


async def download_from_media_site(work: Work) -> Work:
    """
    Asynchronous wrapper for the synchronous download_with_ytdl function.

    Parameters
    ----------
    work : Work
        The Work object representing the video.

    Returns
    -------
    Work
        The updated Work object with the full text (transcript) added.
    """
    loop = asyncio.get_running_loop()
    with Pool(processes=1) as pool:
        result = await loop.run_in_executor(
            None, pool.apply, download_with_ytdl, (work,)
        )
    return result


async def search_and_download_from_media_site(search_input: SearchInput) -> List[Work]:
    """
    Search for videos and download the results.

    This function searches based on the provided search input,
    then downloads and processes each result.

    Parameters
    ----------
    search_input : SearchInput
        The search input containing the query and number of results.

    Returns
    -------
    List[Work]
        A list of Work objects with full text (transcripts) added.
    """
    try:
        logger.info(f"Searching for videos: {search_input.query}")
        search_results = await search_youtube(search_input)
        logger.info(f"Found {len(search_results)} search results")

        if not search_results:
            logger.warning("No search results found")
            return []

        works = []

        for work in search_results:
            try:
                logger.info(f"Downloading and processing video: {work.url}")
                downloaded_work = await download_from_media_site(work)
                if downloaded_work and downloaded_work.full_text:
                    works.append(downloaded_work)
                else:
                    logger.warning(f"Failed to process video: {work.url}")
            except Exception as e:
                logger.error(f"Error processing video {work.url}: {str(e)}")

        logger.info(f"Successfully processed {len(works)} videos")
        return works
    except Exception as e:
        logger.error(f"Error in search_and_download_from_media_site: {str(e)}")
        return []
