import base64
from pathlib import Path

import filetype
from openai import AsyncOpenAI

from audio_bridge_mcp.config import Settings

# MIME type detected from file content -> `input_audio.format` value for OpenAI-compatible APIs.
SUPPORTED_MIME_TYPES = {
    "audio/x-wav": "wav",
    "audio/mpeg": "mp3",
    "audio/mp4": "m4a",
    "audio/x-flac": "flac",
    "audio/ogg": "ogg",
    "audio/aac": "aac",
}

BASE_PROMPT = (
    "Transcribe this audio verbatim. Keep every word in the language and script "
    "it was spoken in (e.g. Tamil in Tamil script, Tanglish as spoken mixed Tamil/English). "
    "Do not translate or summarise. Output only the transcript."
)


class AudioTooLargeError(ValueError):
    pass


class UnsupportedAudioError(ValueError):
    pass


class Transcriber:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = AsyncOpenAI(
            api_key=settings.api_key, base_url=settings.base_url, timeout=settings.timeout_seconds
        )

    def _read_audio(self, path: str) -> tuple[str, str]:
        file = Path(path).expanduser()
        if not file.is_file():
            raise FileNotFoundError(f"Audio file not found: {file}")
        max_bytes = self.settings.max_file_mb * 1024 * 1024
        if file.stat().st_size > max_bytes:
            raise AudioTooLargeError(f"File exceeds the {self.settings.max_file_mb} MB limit")
        content = file.read_bytes()
        detected = filetype.guess(content)
        audio_format = SUPPORTED_MIME_TYPES.get(detected.mime) if detected else None
        if audio_format is None:
            found = detected.mime if detected else "unknown"
            raise UnsupportedAudioError(
                f"Unsupported file content '{found}' (extension '{file.suffix}'). "
                f"Supported: {', '.join(SUPPORTED_MIME_TYPES)}"
            )
        return base64.b64encode(content).decode(), audio_format

    def _build_prompt(self, language_hint: str | None, include_tone: bool) -> str:
        prompt = BASE_PROMPT
        if language_hint:
            prompt += f" The audio is likely in: {language_hint}."
        if include_tone:
            prompt += (
                " After the transcript, add a line starting with 'Tone:' briefly describing "
                "the speaker's emotion and delivery."
            )
        return prompt

    async def transcribe(
        self, path: str, language_hint: str | None = None, include_tone: bool = False, model: str | None = None
    ) -> str:
        data, audio_format = self._read_audio(path)
        response = await self.client.chat.completions.create(
            model=model or self.settings.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self._build_prompt(language_hint, include_tone)},
                        {"type": "input_audio", "input_audio": {"data": data, "format": audio_format}},
                    ],
                }
            ],
        )
        return (response.choices[0].message.content or "").strip()
