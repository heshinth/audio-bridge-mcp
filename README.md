# audio-bridge-mcp

An MCP server that turns audio into text, so models without audio input can still "hear".
It sends the audio file to any audio-capable model through an OpenAI-compatible API
(Gemini, OpenRouter models such as Xiaomi MiMo, etc.) and returns the transcript.

- Any language, including Tamil and code-mixed speech like Tanglish (kept as spoken, never translated)
- Optional language hint and tone description
- Provider-agnostic: switch models by changing environment variables
- stdio transport, files up to 20 MB (configurable)

## Tool

`transcribe_audio(path, language_hint?, include_tone?, model?)`

| Argument | Description |
|---|---|
| `path` | Absolute path to a local audio file (`wav`, `mp3`, `m4a`, `flac`, `ogg`, `aac`). The format is detected from the file content (MIME check), not the extension; files that are not valid audio are rejected |
| `language_hint` | Optional, e.g. `Tamil` or `Tanglish` |
| `include_tone` | Append a short `Tone:` line describing the speaker's emotion and delivery |
| `model` | Override the default model for this call |

## Configuration

Set through environment variables, normally the `env` block of your MCP client.
A `.env` file in the working directory also works.

| Variable | Default | Description |
|---|---|---|
| `AUDIO_API_KEY` | required | API key for the provider |
| `AUDIO_BASE_URL` | `https://generativelanguage.googleapis.com/v1beta/openai/` | OpenAI-compatible endpoint |
| `AUDIO_MODEL` | `gemini-3.5-flash-lite` | Model name used for transcription |
| `AUDIO_MAX_FILE_MB` | `20` | Maximum audio file size |
| `AUDIO_TIMEOUT_SECONDS` | `120` | Request timeout |

The API key and base URL are deliberately not tool arguments, so the calling model never sees them.

Example for OpenRouter:

```
AUDIO_BASE_URL=https://openrouter.ai/api/v1
AUDIO_MODEL=<model slug from the provider>
```

The chosen model must support audio input on that endpoint.

## Install and run

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```bash
# run without installing
uvx --from /path/to/audio-bridge-mcp audio-bridge-mcp

# or install as a command
uv tool install /path/to/audio-bridge-mcp
```

After editing the code, use `uvx --refresh --from ...` or `uv tool install --reinstall ...`.

## MCP client setup

Cursor, Claude Desktop and similar clients (`mcp.json`):

```json
{
  "mcpServers": {
    "audio-bridge": {
      "command": "uv",
      "args": ["--directory", "/path/to/audio-bridge-mcp", "run", "audio-bridge-mcp"],
      "env": {
        "AUDIO_API_KEY": "your-key",
        "AUDIO_BASE_URL": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "AUDIO_MODEL": "gemini-3.5-flash-lite"
      }
    }
  }
}
```

For clients with a form (command, arguments, environment variables), enter `uv` as the
command and each argument above as a separate argument. Use the full path from
`which uv` if the client does not inherit your shell `PATH`.

## Development

```bash
uv sync
AUDIO_API_KEY=your-key uv run audio-bridge-mcp
```

Test with the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx @modelcontextprotocol/inspector -e AUDIO_API_KEY=your-key \
  uv --directory . run audio-bridge-mcp
```

Never print to stdout in the server: stdio transport uses it for protocol messages.

## Layout

```
src/audio_bridge_mcp/
  config.py       settings from environment
  transcriber.py  audio loading, prompt, API call
  server.py       FastMCP tool definition and entry point
```
