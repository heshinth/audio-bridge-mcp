from dataclasses import dataclass

SYSTEM_PROMPT = """\
You are a precise speech transcription engine. Your output is read by another model that cannot hear the audio.

Rules:
- Transcribe verbatim, in the language and script each phrase was spoken in. Tamil stays in Tamil script; \
Tanglish (mixed Tamil/English) stays as spoken, with English words in English. Never translate, summarise or "clean up" the speech.
- Keep filler words, repetitions and false starts only when they carry meaning; do not invent words.
- Mark non-speech that matters in square brackets, e.g. [laughs], [music], [silence]. Use [inaudible] for unclear speech instead of guessing.
- Add natural punctuation and paragraph breaks.
- Output only the transcript in the requested format. No preface, no explanations."""


@dataclass(frozen=True)
class TranscriptionOptions:
    language_hint: str | None = None
    speaker_labels: bool = True
    timestamps: bool = True
    include_tone: bool = False


def build_user_prompt(options: TranscriptionOptions) -> str:
    lines = ["Transcribe the attached audio."]
    if options.language_hint:
        lines.append(f"The audio is likely in: {options.language_hint}.")
    if options.speaker_labels:
        lines.append(
            "Identify distinct speakers and prefix each turn with a consistent label "
            "('Speaker 1:', 'Speaker 2:', ...). Start a new line whenever the speaker changes. "
            "If there is only one speaker, still use 'Speaker 1:'."
        )
    if options.timestamps:
        lines.append(
            "Start each line (each speaker turn, or each sentence for a single speaker) with a "
            "timestamp in [MM:SS] format marking when it begins."
        )
    if options.include_tone:
        lines.append(
            "After the transcript, add a final line starting with 'Tone:' briefly describing "
            "the speakers' emotion and delivery."
        )
    return "\n".join(lines)
