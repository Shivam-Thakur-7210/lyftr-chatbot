import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from litellm import acompletion


project_directory = Path(__file__).resolve().parent.parent
load_dotenv(project_directory / ".env")


async def generate_reply(messages):
    model = os.getenv("LLM_MODEL", "").strip()

    api_keys = [
        key.strip()
        for key in os.getenv("LLM_API_KEYS", "").split(",")
        if key.strip()
    ]

    if not model:
        raise ValueError("Set LLM_MODEL in the root .env file")

    if not api_keys:
        raise ValueError("Set LLM_API_KEYS in the root .env file")

    return await acompletion(
        model=model,
        messages=messages,
        api_key=api_keys[0],
        timeout=float(os.getenv("LLM_TIMEOUT_SECONDS", "30")),
    )


if __name__ == "__main__":
    response = asyncio.run(generate_reply([
        {
            "role": "user",
            "content": "Say hello in one short sentence.",
        }
    ]))

    print("Reply:", response.choices[0].message.content)
    print("Model:", response.model)
    print("Input tokens:", response.usage.prompt_tokens)
    print("Output tokens:", response.usage.completion_tokens)