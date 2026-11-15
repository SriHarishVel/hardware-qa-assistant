# Hardware Q&A Assistant

A Python and Streamlit application that answers natural-language questions about a Linux laptop using Gemini function calling and read-only hardware inspection tools.

## Features

- CPU inspection
- RAM inspection
- Linux root filesystem storage inspection
- GPU detection through `nvidia-smi`, with `lspci` fallback
- Gemini function calling with an explicit allow-list
- Conversational follow-up questions
- Streamlit chat interface
- Direct hardware snapshot panel
- Error handling for missing tools, unavailable hardware data, and API failures

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

Create `.env` from the example:

```bash
cp .env.example .env
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

Streamlit will print a local URL, normally:

```text
http://localhost:8501
```

Open that URL in your browser.

## Example Questions

- Which processor am I using?
- How many logical processors do I have?
- How much RAM is available?
- How much disk space is free?
- Which GPU is visible to Linux?
- Give me a summary of my hardware.
- Compare my available RAM with free disk space.

## Architecture

1. Streamlit receives the user's question.
2. The Gemini chat model determines which hardware inspection tool is needed.
3. Gemini calls one or more functions from `tools.py`.
4. The functions call fixed read-only inspection functions in `hardware.py`.
5. Structured dictionaries are returned to Gemini.
6. Gemini generates a natural-language answer.
7. Streamlit displays the response and preserves conversation history.

## Safety

- No arbitrary shell command execution.
- No shell interpolation or `shell=True`.
- Subprocess calls are restricted to fixed, read-only calls to `nvidia-smi` and `lspci`.
- No root privileges are requested.
- Tool functions only inspect system information.

## Limitations

- In WSL, CPU, memory, and storage values describe the Linux environment and may not represent the complete physical Windows hardware.
- GPU detection depends on WSL GPU support and the availability of `nvidia-smi` or `lspci`.
- `lspci` may identify a graphics device but usually cannot provide reliable VRAM information.
- Gemini is cloud-hosted. Hardware data returned by inspection tools is sent to Google's API for response generation.
- API availability, quotas, and model access depend on the Gemini API account.

## Project Scope

This project is a functional prototype demonstrating LLM-based hardware inspection through predefined tools. It focuses on natural-language interaction, function calling, structured hardware information, and conversational follow-ups.
