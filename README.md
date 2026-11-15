# Hardware Q&A Assistant

A Python and Streamlit application that answers natural-language questions about a Linux laptop using Gemini function calling and predefined read-only hardware inspection tools.

## Features

- CPU inspection
- RAM usage and availability inspection
- Linux root filesystem storage inspection
- GPU detection through `nvidia-smi`, with `lspci` fallback
- Gemini function calling with an explicit tool allow-list
- Conversational follow-up questions
- Streamlit chat interface
- Structured hardware data returned through Python functions
- Error handling for unavailable hardware information, missing tools, and API failures

## Requirements

- Python 3.10+
- Internet connection
- Gemini API key
- Linux environment (Ubuntu/WSL recommended)

## Setup on Ubuntu / WSL

```bash
cd ~/hardware-qa-assistant

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```bash
nano .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key
```

Do not share `.env` or commit it to Git.

## Run

```bash
streamlit run main.py
```

Streamlit will provide a local URL, normally:

```text
http://localhost:8501
```

Open the URL in your browser.

## Example Questions

- Which processor am I using?
- How many logical processors do I have?
- How much RAM is installed?
- How much RAM is currently available?
- How much disk space is free?
- Which GPU is visible to Linux?
- How much GPU memory is available?
- Compare my available RAM with free disk space.
- Summarize my hardware specifications.

## Architecture

1. Streamlit receives the user's natural-language question.
2. The Gemini chat model determines which hardware inspection tool is required.
3. Gemini calls predefined functions from `tools.py`.
4. The functions invoke read-only inspection functions in `hardware.py`.
5. Hardware information is collected and returned as structured Python dictionaries.
6. Gemini generates a natural-language response using the returned information.
7. Streamlit displays the response and maintains conversational context.

## Safety

- No arbitrary shell command execution.
- No `shell=True` or shell interpolation.
- Subprocess calls use predefined commands for GPU detection.
- No root privileges are requested.
- Hardware inspection functions do not intentionally modify system files or settings.
- Only predefined hardware inspection functions are exposed to Gemini.

## Limitations

- In WSL, CPU, memory, and storage values describe the Linux environment and may differ from the physical Windows hardware.
- GPU detection depends on WSL GPU support and the availability of `nvidia-smi` or `lspci`.
- `lspci` may identify a graphics device but generally cannot provide reliable VRAM information.
- The current implementation does not retrieve motherboard RAM slots or maximum supported memory capacity.
- The assistant cannot reliably determine every physical hardware specification from the available inspection tools.
- Gemini is cloud-hosted. Hardware data returned by inspection tools is sent to Google's API for response generation.
- API availability, quotas, and model access depend on the Gemini API account.

## Project Scope

This project is a functional prototype demonstrating natural-language hardware inspection through predefined tools. It focuses on Gemini function calling, safe read-only system inspection, structured hardware information, and conversational follow-ups. The application runs locally in the Linux environment being inspected.
