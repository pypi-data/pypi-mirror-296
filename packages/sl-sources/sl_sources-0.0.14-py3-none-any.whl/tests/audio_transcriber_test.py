import pytest
from sl_sources.audio_transcriber import AudioTranscriber
import asyncio
import os

NAME_OF_PACKAGE: str = "sources"  # TODO: We probably don't want to hardcode this

# Other things to test in future, not worth testing on Aug 12, 2024:
# - Handles audio files with low sampling rates
# - Handles very short and very long audio files (or else raises error on lenghts its not designed for)
# - Does not provide text for silent audio file.

################################# Helper Functions #################################
KEY_WORD_IN_BEULLER_CLIP = "life moves pretty fast"
KEY_WORD_IN_STAR_WARS_CLIP = "Star Wars"
VALID_AUDIO_PATHS_OR_URLS = [  # Modelled as (audio_file_path_or_url, expected_keyword_in_transcription)
    (
        "tests/test_data/audio_transcriber_data/short-clip-buellers-life-moves-pretty-fast.wav",
        KEY_WORD_IN_BEULLER_CLIP,
    ),
    (
        "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav",
        KEY_WORD_IN_BEULLER_CLIP,
    ),
    (
        "tests/test_data/audio_transcriber_data/star_wars_podcast.mp3",
        KEY_WORD_IN_STAR_WARS_CLIP
    ),
    (
        "https://dcs.megaphone.fm/STU5398380055.mp3?key=20757e325545ea9f30567740f86f1cf7&request_event_id=975e70d0-8c85-4b6e-9c2a-915e1017a4cb&timetoken=1723944464_C318A1072E76C4935CEC61B4BC61AE6C",
        KEY_WORD_IN_STAR_WARS_CLIP
    ),
]


def create_transcription_tests_cases() -> list[tuple[str, str, bool]]:
    test_cases = []
    deepgram_enabled_statuses = [True, False]
    for deepgram_enabled in deepgram_enabled_statuses:
        for audio_file_path, expected_keyword in VALID_AUDIO_PATHS_OR_URLS:
            test_cases.append((audio_file_path, expected_keyword, deepgram_enabled))
    return test_cases


##################################### Tests #########################################


@pytest.mark.parametrize(
    "audio_file_path_or_url, expected_keyword, deepgram_enabled",
    create_transcription_tests_cases(),
)
def test_properly_chunks_valid_file_types(
    audio_file_path_or_url: str, expected_keyword: str, deepgram_enabled: bool
) -> None:

    if expected_keyword == KEY_WORD_IN_STAR_WARS_CLIP:
        pytest.skip(
            "The Star wars podcast takes too long to process during unit testing."
        )

    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
    if deepgram_enabled and not deepgram_api_key:
        pytest.skip("Deepgram API key not found.")

    if not deepgram_enabled:
        del os.environ["DEEPGRAM_API_KEY"]

    try:
        if audio_file_path_or_url.startswith("http"):
            absolute_path_or_url = audio_file_path_or_url
        else:
            current_file_path = os.path.abspath(__file__)
            package_path = os.path.dirname(current_file_path)
            while os.path.basename(package_path) != NAME_OF_PACKAGE:
                package_path = os.path.dirname(package_path)
            absolute_path_or_url = str(
                os.path.join(package_path, audio_file_path_or_url)
            )

        transcription_output = asyncio.run(
            AudioTranscriber.transcribe_audio(absolute_path_or_url)
        )

        transcription_duration = transcription_output.audio_duration_in_seconds
        assert transcription_duration > 0

        transcribed_chunks = transcription_output.transcript_chunks
        expected_num_chunks = 2 if transcription_duration > 30 else 1
        assert len(transcribed_chunks) >= expected_num_chunks
        assert all([len(chunk) > 0 for chunk in transcribed_chunks])
        assert expected_keyword.lower() in "".join(transcribed_chunks).lower()

        transcription = transcription_output.transcript
        assert expected_keyword.lower() in transcription.lower()
        assert len(transcription) > 10
        assert isinstance(transcription, str)

        transcription_with_all_spaces_removed = transcription.replace(" ", "").replace(
            "\n", ""
        )
        combined_chunks_with_all_spaces_removed = (
            "".join(transcribed_chunks).replace(" ", "").replace("\n", "")
        )
        assert (
            transcription_with_all_spaces_removed
            == combined_chunks_with_all_spaces_removed
        )
    finally:
        if deepgram_api_key is not None:
            os.environ["DEEPGRAM_API_KEY"] = deepgram_api_key
