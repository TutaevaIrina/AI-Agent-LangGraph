import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

load_dotenv()


def _get_env_var(name: str) -> str | None:
    value = os.getenv(name)
    if not value:
        return None
    cleaned = value.strip()
    return cleaned or None


def _has_newline(value: str) -> bool:
    return "\n" in value or "\r" in value


GROQ_API_KEY = _get_env_var("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

OPENAI_API_KEY = _get_env_var("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()


if LLM_PROVIDER == "groq" and GROQ_API_KEY and not _has_newline(GROQ_API_KEY):
    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.1,
    )
elif LLM_PROVIDER == "openai" and OPENAI_API_KEY:
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0.1,
    )
else:
    raise ValueError(
        "No usable LLM provider configured. Set LLM_PROVIDER to 'groq' or 'openai' and provide the corresponding API key."
    )
