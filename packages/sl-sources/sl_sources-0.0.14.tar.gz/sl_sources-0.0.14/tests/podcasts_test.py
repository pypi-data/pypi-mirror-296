import asyncio
import pytest
import logging
logger = logging.getLogger(__name__)

from sl_ai_models import Gpt4o, clean_indents
from sl_sources.podcasts import (
    PodcastEpisode,
    PodcastSearcher,
    PodcastTranscriber,
    TranscribedEpisode,
)
from sl_sources.models import (
    ENTITY_TYPES,
    SOURCE_TYPES,
    WORK_TYPES,
    Author,
    Publication,
    Publisher,
    SearchInput,
    Work,
)
from sl_sources.podcasts import (
    search_and_download_podcasts,
    search_podcasts,
    download_podcast,
    PodcastEpisode,
)




# Consider making these tests:
# Rank results by relevance
# Search is not blocking (works async)
# Rejects irrelevant prompts
# - If it does not ask for podcast episodes
# - If it does not give insturctions for what type of espisode is desired
# - If there is ambiguity in the prompt
# - If filters that don't exist are requested (filter by date, length, guest speakers, etc



def test_search_podcasts():
    PodcastSearcher._RUN_AGAINST_MOCK_SERVER = True
    try:
        search_input = SearchInput(
            query="Star Wars",
            num_results=1,
            entity_types=[ENTITY_TYPES.WORK, ENTITY_TYPES.AUTHOR, ENTITY_TYPES.PUBLICATION],
        )
        results = asyncio.run(search_podcasts(search_input))

        assert len(results) > 0
        assert any(isinstance(entity, Work) for entity in results)
        assert any(isinstance(entity, Author) for entity in results)
        assert any(isinstance(entity, Publication) for entity in results)
    finally:
        PodcastSearcher._RUN_AGAINST_MOCK_SERVER = False

def test_download_podcast():
    episode = PodcastEpisode(
        podcast_title="Test Podcast",
        episode_title="Test Episode",
        description="Test episode description",
        audio_url="https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav",
        audio_length_seconds=1800,
        other_data={
            "id": "1234",
            "link": "https://example.com/test_episode",
            "podcast": {
                "id": "5678",
                "title": "Test Podcast",
                "website": "https://example.com/test_podcast",
            },
        },
    )
    work = asyncio.run(download_podcast(episode))

    assert isinstance(work, Work)
    assert work.name == episode.episode_title
    assert work.abstract == episode.description
    assert work.url == episode.other_data["link"]
    assert work.source_type == SOURCE_TYPES.PODCAST
    assert work.work_type == WORK_TYPES.PODCAST
    assert len(work.full_text) > 0
    assert len(work.authors) == 1
    assert work.authors[0].name == episode.podcast_title
    assert len(work.publications) == 1
    assert work.publications[0].name == episode.podcast_title


def test_search_and_download_podcasts():
    PodcastSearcher._RUN_AGAINST_MOCK_SERVER = True
    try:
        search_input = SearchInput(
            query="Star Wars",
            num_results=1,
            entity_types=[
                ENTITY_TYPES.WORK,
                ENTITY_TYPES.AUTHOR,
                ENTITY_TYPES.PUBLICATION,
                ENTITY_TYPES.PUBLISHER,
            ],
        )
        entities = asyncio.run(search_and_download_podcasts(search_input))

        assert (
            len(entities) > 1
        )  # Should include works, authors, publications, and possibly publishers
        assert any(isinstance(entity, Work) for entity in entities)
        assert any(isinstance(entity, Author) for entity in entities)
        assert any(isinstance(entity, Publication) for entity in entities)

        works = [entity for entity in entities if isinstance(entity, Work)]
        assert len(works) > 0
        for work in works:
            assert isinstance(work, Work)
            assert len(work.full_text) > 0
            assert len(work.authors) > 0
            assert len(work.publications) > 0
    finally:
        PodcastSearcher._RUN_AGAINST_MOCK_SERVER = False


def create_topic_prompt(topic: str) -> str:
    return f"Please find me podcasts related to the topic '{topic}' as it relates to the intersection of AI Safety (making sure AI helps and does not harm people) and Neurotech (Neuroscience, technology applications to neuroscience, etc). The goal is to use these podcasts to gather information for a professional research report covering the topic mentioned to help researchers and policy makers understand the field."


@pytest.mark.skip(
    reason="These tests are a slow and expensive. Run then on a as-needed basis"
)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "prompt",
    [
        create_topic_prompt("Neurotech-Enhanced AI Decision Making"),
        create_topic_prompt("Cognitive Overload and Dependence"),
        create_topic_prompt("Neurosecurity"),
        create_topic_prompt("Impact on Human Identity and Agency"),
        create_topic_prompt("Real-Time Cognitive Load Balancing in AI Systems"),
        create_topic_prompt("User Training and Adaptation"),
        create_topic_prompt("Neurological Data Integrity in AI Systems"),
    ],
)
@pytest.mark.asyncio
async def test_search_and_transcribe_returns_relevant_results(prompt: str) -> None:
    # Search for podcast episodes
    podcasts = await PodcastSearcher.smart_search_for_podcast_episodes(prompt)
    logger.info(
        f"Found {len(podcasts)} podcasts:\n {[podcast.model_dump_json() for podcast in podcasts]}"
    )

    # Assert that we have enough unique results
    assert len(podcasts) >= 5, "Not enough podcast episodes returned"
    assert len(set([result.audio_url for result in podcasts])) == len(
        podcasts
    ), "Duplicate episodes found"

    # Assess relevance of each podcast
    assessment_tasks = [
        assess_if_podcast_fulfills_prompt(prompt, podcast) for podcast in podcasts
    ]
    results = await asyncio.gather(*assessment_tasks)

    # Process assessment results
    answers, explanations = zip(*results)
    percent_correct = sum(answers) / len(answers)
    logger.info(f"Percent of relevant podcasts: {percent_correct:.2%}")

    transcription_report = ""
    summary_report = ""
    for podcast, answer, explanation in zip(podcasts, answers, explanations):
        transcription_report += f"----------------------\nPodcast: {podcast.episode_title}\nAnswer: {answer}\n\nExplanation: \n{explanation}\n\nDescrption:\n {podcast.description}\n\nTranscription:\n {podcast.transcript}\n\n"
        summary_report += f"Podcast: {podcast.episode_title}\nAnswer: {answer}\n\n"

    logger.info(transcription_report)
    logger.info(summary_report)
    logger.info(f"Percent of relevant podcasts: {percent_correct:.2%}")

    assert (
        percent_correct >= 0.5
    ), f"Only {percent_correct:.2%} of the podcasts matched the prompt"


async def assess_if_podcast_fulfills_prompt(
    input_prompt: str, podcast: TranscribedEpisode
) -> tuple[bool, str]:
    prompt = clean_indents(f"""
        You are a manager evaluating work of an intern. The intern was asked to do the following:
        ```
        {input_prompt}
        ```

        One of the podcasts they returned was:
        ```
        Name: {podcast.episode_title}
        Description: {podcast.description}
        Audio URL: {podcast.audio_url}
        Transcription:
        {podcast.transcript}
        ```

        You must determine if the intern found a podcast that matches the instructions given to them.
        Take it step by step
        1) Summarize the podcast in your own words, paying attention to the prompt
        2) List out the requirements inferred by the prompt
        3) For each requirement determine if the podcast meets the requirement
        4) Finally return a json with your reasoning for your final assessment. Your assessment should be either TRUE or FALSE.

        Example JSON output:
        ```
        {{
            "reasoning": "...reasoning here step by step...",
            "assessment": "TRUE"
        }}
        ```

        Give your final assessment as a JSON. Your response must include the JSON block or it will not be accepted.
        """)
    model = Gpt4o(temperature=0)
    response = await model.invoke_and_return_verified_type(prompt, dict)
    reasoning = response["reasoning"]
    assessment = response["assessment"]
    logger.info(f"Assessment for {podcast.episode_title}: {assessment}. Reasoning: {reasoning}")
    return assessment == "TRUE", reasoning

def test_key_word_search_works_against_mock_server() -> None:
    PodcastSearcher._RUN_AGAINST_MOCK_SERVER = True
    try:
        search = "Prompt doesn't matter for mock server"
        episodes = asyncio.run(
            PodcastSearcher.key_word_search_for_podcast_episodes(search)
        )
        assert len(episodes) > 0
        assert len(set([result.audio_url for result in episodes])) == len(episodes)
        assert any(["star wars" in result.description.lower() for result in episodes])
        assert any(["star wars" in result.episode_title.lower() for result in episodes])
    finally:
        PodcastSearcher._RUN_AGAINST_MOCK_SERVER = False


def test_errors_if_no_input() -> None:
    prompt = ""
    with pytest.raises(ValueError):
        asyncio.run(PodcastSearcher.smart_search_for_podcast_episodes(prompt))


def test_transcription_returns_valid_transcribed_episode() -> None:
    episode = PodcastEpisode(
        podcast_title="Test Podcast",
        episode_title="Test Episode",
        description="Test Description",
        audio_url="https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav",
        audio_length_seconds=12 * 60,
    )
    transcribed_episode = asyncio.run(PodcastTranscriber.transcribe_episode(episode))
    assert isinstance(transcribed_episode, TranscribedEpisode)
    assert transcribed_episode.podcast_title == episode.podcast_title
    assert transcribed_episode.episode_title == episode.episode_title
    assert transcribed_episode.description == episode.description
    assert transcribed_episode.audio_url == episode.audio_url
    logger.info(f"Transcribed parts: {transcribed_episode.transcript_chunks}")
    assert len(transcribed_episode.transcript_chunks) > 0
    assert all([len(chunk) > 0 for chunk in transcribed_episode.transcript_chunks])
    key_word_expected_in_podcast = "life moves pretty fast"
    assert (
        key_word_expected_in_podcast.lower() in transcribed_episode.transcript.lower()
    )
