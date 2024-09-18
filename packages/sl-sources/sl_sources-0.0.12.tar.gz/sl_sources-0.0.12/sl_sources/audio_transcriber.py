import logging
import os
import tempfile
import aiohttp
import librosa
import numpy as np
from pydantic import BaseModel
from tqdm import tqdm
from sl_ai_models import DeepgramNova2
from sl_ai_models.deepgram_nova2 import DeepgramOutput
import asyncio

logger = logging.getLogger(__name__)

import librosa
from tqdm import tqdm


def transcribe(audio_file_path_or_audio_url: str) -> str:
    transcription_output = asyncio.run(
        AudioTranscriber.transcribe_audio(audio_file_path_or_audio_url)
    )
    transcription = transcription_output.transcript
    return transcription


class AudioTranscriptionOutput(BaseModel):
    transcript_chunks: list[str]
    audio_duration_in_seconds: float
    other_metadata: dict | None = None

    @property
    def transcript(self) -> str:
        return "\n\n".join(self.transcript_chunks)


class AudioTranscriber:
    _TARGET_RESAMPLING_RATE_IN_HZ = 16000

    @classmethod
    async def transcribe_audio(
        cls, audio_file_absolute_path_or_url: str
    ) -> AudioTranscriptionOutput:
        logger.info(f"Transcribing audio file '{audio_file_absolute_path_or_url}'.")
        input_is_url = audio_file_absolute_path_or_url.startswith("http")
        input_is_file = os.path.exists(audio_file_absolute_path_or_url)
        assert (
            input_is_url or input_is_file
        ), f"Input '{audio_file_absolute_path_or_url}' is not a valid URL or file path."

        deepgram_enabled = os.getenv("DEEPGRAM_API_KEY") is not None
        if deepgram_enabled:
            transcription_chunks, deepgram_output = (
                await cls.__audio_to_chunked_transcript_with_deepgram(
                    audio_file_absolute_path_or_url
                )
            )
            audio_duration_in_seconds = deepgram_output.audio_duration_in_seconds
            other_metadata = deepgram_output.model_dump()
        elif input_is_url:
            transcription_chunks, duration = (
                await cls.__audio_url_to_chunked_transcript_with_whisper(
                    audio_file_absolute_path_or_url
                )
            )
            audio_duration_in_seconds = duration
            other_metadata = None
        else:
            transcription_chunks, duration = (
                await cls.__audio_file_path_to_chunked_transcript_with_whisper(
                    audio_file_absolute_path_or_url
                )
            )
            audio_duration_in_seconds = duration
            other_metadata = None

        output = AudioTranscriptionOutput(
            transcript_chunks=transcription_chunks,
            audio_duration_in_seconds=audio_duration_in_seconds,
            other_metadata=other_metadata,
        )
        logger.debug(
            f"Transcription complete for audio '{audio_file_absolute_path_or_url}'."
        )
        logger.debug(f"Transcription output: {output}")
        return output

    @classmethod
    async def __audio_to_chunked_transcript_with_deepgram(
        cls, audio_file_aboslute_path: str
    ) -> tuple[list[str], DeepgramOutput]:
        logger.debug(
            f"Transcribing audio file '{audio_file_aboslute_path}' with Deepgram."
        )
        model = DeepgramNova2()
        transcription_output = await model.invoke(audio_file_aboslute_path)
        transcript = transcription_output.transcript
        transcription_chunks = [chunk for chunk in transcript.split("\n") if chunk]
        return transcription_chunks, transcription_output

    @classmethod
    async def __audio_url_to_chunked_transcript_with_whisper(
        cls, audio_url: str
    ) -> tuple[list[str], float]:
        assert audio_url.startswith("http"), f"Input '{audio_url}' is not a valid URL."
        logger.debug(f"Trying to get audio file from '{audio_url}'.")
        async with aiohttp.ClientSession() as session:
            async with session.get(audio_url) as response:
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(
                    suffix=".mp3", delete=True
                ) as temp_file:
                    temp_file.write(await response.read())
                    temp_file.flush()
                    logger.debug(
                        f"Got audio file for '{audio_url}'. Starting transcription"
                    )
                    transcription_chunks, duration = (
                        await cls.__audio_file_path_to_chunked_transcript_with_whisper(
                            temp_file.name
                        )
                    )
                    return transcription_chunks, duration

    @classmethod
    async def __audio_file_path_to_chunked_transcript_with_whisper(
        cls, audio_file_aboslute_path: str
    ) -> tuple[list[str], float]:
        assert os.path.exists(audio_file_aboslute_path), f"Input '{audio_file_aboslute_path}' is not a valid file path."
        logger.debug(f"Transcribing audio file '{audio_file_aboslute_path}' with Whisper.")
        audio_data = (
            cls.__load_audio_file_as_amplitude_array_using_target_sampling_rate(
                audio_file_aboslute_path
            )
        )
        chunk_length_in_seconds = 30
        audio_data_chunks = cls.__chunk_audio_data_into_equal_pieces(
            audio_data, chunk_length_in_seconds
        )
        duration = len(audio_data_chunks) * chunk_length_in_seconds
        transcription_chunks = await cls.__transcribe_audio_chunks_with_whisper(
            audio_data_chunks
        )
        return transcription_chunks, duration

    @classmethod
    def __load_audio_file_as_amplitude_array_using_target_sampling_rate(
        cls, audio_file_path: str
    ) -> np.ndarray:
        audio_data, sampling_rate = librosa.load(audio_file_path)
        resampled_audio = librosa.resample(
            audio_data,
            orig_sr=sampling_rate,
            target_sr=AudioTranscriber._TARGET_RESAMPLING_RATE_IN_HZ,
        )
        return resampled_audio

    @classmethod
    def __chunk_audio_data_into_equal_pieces(
        cls, audio_data: np.ndarray, chunk_length_in_seconds: int
    ) -> list[np.ndarray]:
        chunk_length_samples = (
            chunk_length_in_seconds * cls._TARGET_RESAMPLING_RATE_IN_HZ
        )
        audio_chunks = [
            audio_data[i : i + chunk_length_samples]
            for i in range(0, len(audio_data), chunk_length_samples)
        ]
        return audio_chunks

    @classmethod
    async def __transcribe_audio_chunks_with_whisper(
        cls, audio_chunks: list[np.ndarray]
    ) -> list[str]:
        from transformers import WhisperForConditionalGeneration, WhisperProcessor
        from transformers.generation.utils import GenerateOutput

        processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")
        assert isinstance(processor, WhisperProcessor)

        model = WhisperForConditionalGeneration.from_pretrained(
            "openai/whisper-small.en"
        )

        transcription_chunks = []
        for chunk in tqdm(audio_chunks, desc="Transcribing"):
            inputs = processor(
                chunk,
                sampling_rate=cls._TARGET_RESAMPLING_RATE_IN_HZ,
                return_tensors="pt",
            )

            if "input_features" in inputs:
                input_features = inputs["input_features"]
            else:
                raise ValueError(
                    "The processor output does not contain 'input_features'."
                )

            output = model.generate(
                input_features,
                output_scores=False,
                return_dict_in_generate=True,
                output_attentions=False,
            )
            assert isinstance(output, GenerateOutput)

            for sequence in output.sequences:
                chunk_text = processor.decode(sequence, skip_special_tokens=True)
                transcription_chunks.append(chunk_text)

        return transcription_chunks
