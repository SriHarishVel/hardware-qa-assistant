
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import ALL_TOOLS

load_dotenv()

MODEL = "gemini-3.6-flash"

SYSTEM_PROMPT = """
You are a Linux Hardware Q&A Assistant.

Help users understand their computer's hardware.

TOOL USE:
- Use the appropriate inspection tool when actual hardware information is required.
- Use multiple tools when necessary.
- Treat tool output as the source of truth.
- Never invent missing hardware information.
- Explain clearly when information is unavailable.

ACCURACY:
- Distinguish logical processors from physical CPU cores.
- Distinguish total, used, and available RAM.
- Distinguish disk storage from RAM.
- Storage information refers to the Linux root filesystem.
- In WSL, Linux-visible resources may differ from physical Windows hardware.
- Never infer GPU memory from a GPU model name.
- If GPU detection fails, do not claim that no GPU exists.

SAFETY:
- Only use the supplied hardware inspection tools.
- Never execute arbitrary shell commands.
- Never modify system files or settings.
- Never request root privileges.

PRIVACY:
- Hardware information returned by inspection tools is sent to the configured Gemini API.
- Do not claim that processing is fully local.

STYLE:
- Answer directly and concisely.
- Include appropriate units.
- Explain important limitations.
- Maintain conversational context for follow-up questions.
"""

st.set_page_config(
    page_title="Hardware Q&A Assistant",
    page_icon="🖥️",
    layout="wide",
)

st.title("🖥️ Hardware Q&A Assistant")
st.caption("Ask questions about your Linux laptop and its hardware.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Add GEMINI_API_KEY to your .env file.")
    st.stop()


@st.cache_resource(show_spinner=False)
def create_client(key: str):
    return genai.Client(
        api_key=key,
        http_options={"timeout": 60000},
    )


client = create_client(api_key)


def create_chat():
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=ALL_TOOLS,
        ),
    )


if "chat" not in st.session_state:
    st.session_state.chat = create_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.header("Controls")
    st.caption(f"Model: `{MODEL}`")

    if st.button("New conversation", use_container_width=True):
        st.session_state.chat = create_chat()
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(
        "Hardware information returned by inspection tools "
        "is sent to Google's Gemini API."
    )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Ask about your hardware...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Checking your hardware..."):
                response = st.session_state.chat.send_message(prompt)

            answer = response.text or (
                "I couldn't generate a response. Please try again."
            )

            st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as exc:
            st.error(
                f"Request failed ({type(exc).__name__}). "
                "The Gemini service may be unavailable or the request may have timed out."
            )

            with st.expander("Technical details"):
                st.code(str(exc))
