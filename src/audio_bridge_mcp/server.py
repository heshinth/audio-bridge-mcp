from fastmcp import FastMCP

from audio_bridge_mcp.config import load_settings
from audio_bridge_mcp.prompt import TranscriptionOptions
from audio_bridge_mcp.transcriber import Transcriber

mcp = FastMCP("Audio Bridge MCP")


def main() -> None:
    transcriber = Transcriber(load_settings())

    @mcp.tool
    async def transcribe_audio(
        path: str,
        language_hint: str | None = None,
        speaker_labels: bool = True,
        timestamps: bool = True,
        include_tone: bool = False,
        model: str | None = None,
    ) -> str:
        """Transcribe a local audio file (wav, mp3, m4a, flac, ogg, aac; max 20 MB) to text.

        Works with any language, including Tamil and code-mixed speech like Tanglish.

        Args:
            path: Absolute path to the audio file.
            language_hint: Optional hint such as "Tamil" or "Tanglish".
            speaker_labels: Label each turn as "Speaker 1:", "Speaker 2:", ... (diarization).
            timestamps: Prefix each line with an approximate [MM:SS] start time.
            include_tone: Append a short description of the speaker's tone.
            model: Override the default model for this call.
        """
        options = TranscriptionOptions(language_hint, speaker_labels, timestamps, include_tone)
        return await transcriber.transcribe(path, options, model)

    mcp.run()


if __name__ == "__main__":
    main()
