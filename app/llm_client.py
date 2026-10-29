import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada")

    return OpenAI(
        api_key=api_key,
        timeout=20.0,
        max_retries=0,
    )