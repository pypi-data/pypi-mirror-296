import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional

import aiohttp
from listennotes import podcast_api
from pydantic import BaseModel

from .audio_transcriber import AudioTranscriber
from sl_ai_models import Gpt4o, clean_indents
from .models import (
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

logger = logging.getLogger(__name__)


class PodcastEpisode(BaseModel):
    podcast_title: str
    episode_title: str
    description: str
    audio_url: str
    audio_length_seconds: int
    other_data: dict | None = None


class TranscribedEpisode(PodcastEpisode):
    transcript_chunks: list[str]

    @property
    def transcript(self) -> str:
        return "\n".join(self.transcript_chunks)


class PodcastSearcher:
    """
    The podcast searcher uses ListenNotes API.
    We had to apply to get access to ListenNotes. They approved saving transcripts and podcast metadata, however under the terms of use, we are not necessarily allowed to display or cache podcast data for other uses.
    Please reference the terms of service if using podcast data for anything other than transcript quoting. https://www.listennotes.com/api/terms/

    API Docs can be found here: https://www.listennotes.com/api/docs/?lang=python&test=0#get-api-v2-search
    """

    _RUN_AGAINST_MOCK_SERVER: bool = False

    @classmethod
    async def smart_search_for_podcast_episodes(
        cls, prompt_asking_for_type_of_episode: str
    ) -> list[TranscribedEpisode]:
        logger.info(
            f"Searching for podcast episodes based on the prompt: {prompt_asking_for_type_of_episode}"
        )
        if prompt_asking_for_type_of_episode == "":
            raise ValueError("The key word query cannot be empty.")

        key_words = await cls.__generate_keywords(prompt_asking_for_type_of_episode)
        episodes = await cls.__search_for_podcast_episodes(key_words)
        unique_episodes = cls.__find_unique_episodes_in_list(episodes)
        relevance_predictions = await cls.__predict_relevance(
            prompt_asking_for_type_of_episode, unique_episodes
        )
        episodes_to_transcribe = (
            cls.__select_episodes_for_transcription_based_on_relevance(
                unique_episodes, relevance_predictions
            )
        )
        transcribed_episodes = await cls.__transcribe_episodes(episodes_to_transcribe)

        return transcribed_episodes

    @classmethod
    async def __generate_keywords(
        cls, prompt_asking_for_type_of_episode: str
    ) -> list[str]:
        prompt = clean_indents(f"""
            You are a professional researcher who has been given the following instructions:
            ```
            {prompt_asking_for_type_of_episode}
            ```

            You are being paid by the hour, but will be given a $200 tip if you can find some really good informational gems.

            You have been asked to find podcast episodes that match the instructions given to you.
            Your first goal is to run a search on ListenNotes, a podcast database.
            ListenNotes does not use semantic search, and so you have to choose keywords and choose them carefully.
            You must find a balance between being too specific and too general.
            Being too specific may result in no results, while being too general may result in irrelevant results.
            ListenNotes searches for keywords in episode title, podcast name, episode description, author, and transcript

            Lets take this step by step:
            1) Consider what you know about the topic, and specific orgs, events, entities, people, etc. that are relevant.
            2) Based on what you know decide on 3 keywords or phrases that you think will help you find the right podcast episodes.
            3) Give your answer as a list of strings, each string being a keyword or phrase. Do not include any other words other than the list of strings

            For example if you were asked to find podcasts about "Economic perils in the The history of the United States" you would answer:
            ```
            [
                "Economic problems history United States",
                "Great depression, 2008 recession, stock market crash",
                "Economic history of America"
            ]
            ```

            Respond with a JSON block containing an array of strings.
            """)

        model = Gpt4o(temperature=0)
        key_words: list[str] = await model.invoke_and_return_verified_type(prompt, list[str])
        logger.info(f"Generated key words: {key_words}")
        return key_words

    @classmethod
    async def __search_for_podcast_episodes(
        cls, key_words: list[str]
    ) -> list[PodcastEpisode]:
        async def search_wrapper(key_word: str) -> list[PodcastEpisode]:
            try:
                return await cls.key_word_search_for_podcast_episodes(key_word)
            except Exception as e:
                logger.error(
                    f"An error occurred while searching for podcast episodes: {e}"
                )
                return []

        tasks = [search_wrapper(key_word) for key_word in key_words]
        episodes_lists = await asyncio.gather(*tasks)
        flattened_episodes = [episode for sublist in episodes_lists for episode in sublist]
        logger.info(
            f"Found {len(flattened_episodes)} podcast episodes from {len(key_words)} keyword searches"
        )
        return flattened_episodes

    @classmethod
    def __find_unique_episodes_in_list(
        cls, episodes: list[PodcastEpisode]
    ) -> list[PodcastEpisode]:
        unique_episodes = []
        set_of_title_podcast_pairs = set()
        for episode in episodes:
            title_podcast_combined = episode.episode_title + episode.podcast_title
            if title_podcast_combined not in set_of_title_podcast_pairs:
                set_of_title_podcast_pairs.add(title_podcast_combined)
                unique_episodes.append(episode)
        return unique_episodes

    @classmethod
    async def __predict_relevance(
        cls, prompt_asking_for_type_of_episode: str, episodes: list[PodcastEpisode]
    ) -> list[float]:
        async def predict_wrapper(episode: PodcastEpisode) -> float:
            try:
                return await cls.__determine_relevance_of_podcast(
                    prompt_asking_for_type_of_episode, episode
                )
            except Exception as e:
                logger.error(
                    f"An error occurred while predicting relevance of podcast episode assigning relevance to 0: {e}"
                )
                return 0.0

        relevance_tasks = [predict_wrapper(episode) for episode in episodes]
        relevance_predictions = await asyncio.gather(*relevance_tasks)
        logger.info(
            f"Successfully predicted relevance of {len(relevance_predictions)} out of {len(episodes)} podcast episodes"
        )
        return relevance_predictions

    @classmethod
    async def __determine_relevance_of_podcast(
        cls, prompt: str, episode: PodcastEpisode
    ) -> float:
        model = Gpt4o(temperature=0)
        prompt = clean_indents(f"""
            You are a professional researcher who has been given the following instructions:
            ```
            {prompt}
            ```

            In your research you have found a number of different podcasts. One of the podcast Episodes you found was:
            ```
            **Podcast Title**: {episode.podcast_title}
            **Episode Title**: {episode.episode_title}
            **Description**:
            {episode.description}
            ```

            Your job is determine if the podcast is worth listening to.
            You can only tell so much from just the title and description, but we dont have time to listen to every podcast we found.
            Please give a prediction of how likely it is that you would pick this podcast to share with your boss after listening to it (i.e. it fulfills the instructions)

            Your prediction should be a number between 0 and 1, where 0 is not at all likely, and 1 is very likely.
            0 would mean you are certain right now that you would not share it.
            0.1 would mean you are very unlikely to share it.
            0.3 would mean that you are unlikely to share it.
            0.5 would mean that it really depends on the content.
            0.7 would mean that you are likely to share it.
            0.9 would mean that you are very likely to share it.
            1.0 would means that you can tell right now from the title and description that you would share it.

            Your boss will take a random sample of your predictions and you will be paid a $200 tip if your prediction is accurate overall.

            Take this step by step:
            1) Consider the requirements inferred by the instructions you were given.
            2) Consider the title and description of the podcast episode and how well it meets the requirements.
            3) Consider how likely you would be to share this podcast with your boss after listening to it.
            4) Give your answer as a json. Don't give any other information other than the json.

            For example, if you found an episode you were likely to share you would answer:
            {{
                "reasoning": "...add your reasoning here..."
                "prediction": 0.7
            }}
            Remember only give the json and no other words around it. Do all your steps in the reasoning section.
            """)
        response = await model.invoke_and_return_verified_type(prompt, dict[str,Any])
        reasoning = response["reasoning"]
        final_prediction = float(response["prediction"])
        logger.debug(
            f"Relevance prediction for episode {episode.episode_title}: {final_prediction}. Reasoning:\n {reasoning}"
        )
        assert (
            final_prediction <= 1
        ), "The prediction must be between 0 and 1"
        assert (
            final_prediction >= 0
        ), "The prediction must be between 0 and 1"
        return final_prediction


    @classmethod
    def __select_episodes_for_transcription_based_on_relevance(
        cls, episodes: list[PodcastEpisode], relevance_predictions: list[float]
    ) -> list[PodcastEpisode]:
        episode_relevance_pairs_sorted_by_relevance = sorted(
            zip(episodes, relevance_predictions), key=lambda x: x[1], reverse=True
        )
        episodes_greater_than_0_5_relevance = [
            episode
            for episode, relevance in episode_relevance_pairs_sorted_by_relevance
            if relevance > 0.5
        ]
        top_10_episodes = [
            episode for episode, _ in episode_relevance_pairs_sorted_by_relevance[:10]
        ]
        episodes_to_transcribe = (
            episodes_greater_than_0_5_relevance
            if len(episodes_greater_than_0_5_relevance) > len(top_10_episodes)
            else top_10_episodes
        )
        return episodes_to_transcribe

    @classmethod
    async def __transcribe_episodes(
        cls, episodes_to_transcribe: list[PodcastEpisode]
    ) -> list[TranscribedEpisode]:
        async def transcribe_wrapper(episode: PodcastEpisode) -> TranscribedEpisode:
            try:
                return await PodcastTranscriber.transcribe_episode(episode)
            except Exception as e:
                logger.error(
                    f"An error occurred while transcribing podcast episode: {e}"
                )
                return TranscribedEpisode(**episode.model_dump(), transcript_chunks=[])

        transcribe_tasks = [
            transcribe_wrapper(episode) for episode in episodes_to_transcribe
        ]
        transcribed_episodes = await asyncio.gather(*transcribe_tasks)
        logger.info(
            f"Successfully transcribed {len(transcribed_episodes)} out of {len(episodes_to_transcribe)} podcast episodes"
        )
        return transcribed_episodes

    @classmethod
    async def key_word_search_for_podcast_episodes(
        cls, key_word_query: str
    ) -> list[PodcastEpisode]:
        if key_word_query == "":
            raise ValueError("The key word query cannot be empty.")

        if cls._RUN_AGAINST_MOCK_SERVER:
            listen_notes_api_key = None
        else:
            listen_notes_api_key = os.getenv("LISTEN_NOTES_API_KEY")
            assert listen_notes_api_key is not None, "ListenNotes API key is not set"
        client = podcast_api.Client(api_key=listen_notes_api_key)
        response = client.search(
            q=key_word_query,
            sort_by_date=0,  # 0 for sort by relevance, 1 for date
            type="episode",
            offset=0,  # number of items to skip for pagination
            len_min=0,  # minimum audio length in minutes
            len_max=600,  # maximum audio length in minutes
            language="English",
            page_size=10,  # number of items to return (a number 1 through 10)
            # genre_ids='68,82',
            # published_before=1580172454000,
            # published_after=0,
            # only_in='title,description',
        )
        results = response.json()["results"]
        podcast_episodes = []
        for result in results:
            episode = PodcastEpisode(
                podcast_title=result["podcast"]["title_original"],
                episode_title=result["title_original"],
                description=result["description_original"],
                audio_url=result["audio"],
                audio_length_seconds=result["audio_length_sec"],
                other_data=result,
            )
            podcast_episodes.append(episode)
        if cls._RUN_AGAINST_MOCK_SERVER:
            podcast_episodes = podcast_episodes[:1] # Choose only one for sake of transcription tests taking too long with more than 1
        return podcast_episodes


class PodcastTranscriber:

    @staticmethod
    async def transcribe_episode(episode: PodcastEpisode) -> TranscribedEpisode:
        if isinstance(episode, TranscribedEpisode):
            return episode
        logger.info(
            f"Transcribing episode: '{episode.episode_title}' from podcast: '{episode.podcast_title}' with length {episode.audio_length_seconds/60} minutes"
        )
        transcription_output = await AudioTranscriber.transcribe_audio(
            episode.audio_url
        )
        transcription_chunks = transcription_output.transcript_chunks
        logger.info(f"Transcribed episode: {episode.episode_title}")
        logger.debug(f"Transcription: {transcription_chunks}")
        return TranscribedEpisode(
            podcast_title=episode.podcast_title,
            episode_title=episode.episode_title,
            description=episode.description,
            audio_url=episode.audio_url,
            audio_length_seconds=episode.audio_length_seconds,
            other_data=episode.other_data,
            transcript_chunks=transcription_chunks,
        )


async def search_podcasts(search_input: SearchInput) -> List[Entity]:
    query = search_input.query
    num_results = search_input.num_results
    entity_types = search_input.entity_types

    prompt = f"Find podcast episodes about {query}"
    episodes = await PodcastSearcher.smart_search_for_podcast_episodes(prompt)

    entities: List[Entity] = []
    for episode in episodes[:num_results]:
        if ENTITY_TYPES.WORK in entity_types:
            work = Work(
                id=episode.other_data["id"],
                name=episode.episode_title,
                url=episode.other_data["link"],
                abstract=episode.description,
                source_type=SOURCE_TYPES.PODCAST,
                work_type=WORK_TYPES.PODCAST,
            )
            entities.append(work)
        if ENTITY_TYPES.AUTHOR in entity_types:
            author = Author(
                id=episode.other_data["podcast"]["id"],
                name=episode.podcast_title,
                source_type=SOURCE_TYPES.PODCAST,
            )
            entities.append(author)
        if ENTITY_TYPES.PUBLICATION in entity_types:
            publication = Publication(
                id=episode.other_data["podcast"]["id"],
                name=episode.podcast_title,
                source_type=SOURCE_TYPES.PODCAST,
            )
            entities.append(publication)
        if ENTITY_TYPES.PUBLISHER in entity_types:
            publisher_name = episode.other_data["podcast"].get("publisher_original")
            if publisher_name:
                publisher = Publisher(
                    id=f"publisher_{publisher_name}",  # Create a unique ID
                    name=publisher_name,
                    source_type=SOURCE_TYPES.PODCAST,
                )
                entities.append(publisher)


    return entities


async def download_podcast(episode: PodcastEpisode) -> Work:
    transcribed_episode = await PodcastTranscriber.transcribe_episode(episode)
    publisher_name = episode.other_data["podcast"].get("publisher_original")

    return Work(
        id=episode.other_data["id"],
        name=episode.episode_title,
        url=episode.other_data["link"],
        abstract=episode.description,
        full_text=transcribed_episode.transcript,
        source_type=SOURCE_TYPES.PODCAST,
        work_type=WORK_TYPES.PODCAST,
        authors=[
            Author(
                id=episode.other_data["podcast"]["id"],
                name=episode.podcast_title,
                source_type=SOURCE_TYPES.PODCAST,
            )
        ],
        institutions=[],
        publications=[
            Publication(
                id=episode.other_data["podcast"]["id"],
                name=episode.podcast_title,
                source_type=SOURCE_TYPES.PODCAST,
            )
        ],
        publishers=(
            [
                Publisher(
                    id=f"publisher_{publisher_name}" if publisher_name else None,
                    name=publisher_name,
                    source_type=SOURCE_TYPES.PODCAST,
                )
            ]
            if publisher_name
            else []
        ),
    )


async def search_and_download_podcasts(search_input: SearchInput) -> List[Entity]:
    search_results = await PodcastSearcher.smart_search_for_podcast_episodes(
        search_input.query
    )

    entities: List[Entity] = []
    for episode in search_results[: search_input.num_results]:
        work = await download_podcast(episode)
        entities.append(work)

        if ENTITY_TYPES.AUTHOR in search_input.entity_types:
            entities.extend(work.authors)
        if ENTITY_TYPES.PUBLICATION in search_input.entity_types:
            entities.extend(work.publications)
        if ENTITY_TYPES.PUBLISHER in search_input.entity_types:
            entities.extend(work.publishers)

    return entities
