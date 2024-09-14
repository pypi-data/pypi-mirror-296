import subprocess
from pathlib import Path

from langchain_core.messages import (  # type: ignore
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI  # type: ignore
from pydantic.v1 import SecretStr

from autogen_readme import console


def openai_chat_model(
    human_prompt: str, openai_api_key: SecretStr, temperature: float = 0.0
) -> str:
    chat = ChatOpenAI(
        model="gpt-4o-mini", api_key=openai_api_key, temperature=temperature
    )
    prompt = [
        SystemMessage(
            content="You are a helpful assistant, with a focus on Python code and documentation writing."
        ),
        HumanMessage(content=human_prompt),
    ]
    response: BaseMessage = chat.invoke(prompt)
    return str(response.content)


def execute_local_script(script_path: Path, prompt: str) -> str:
    try:
        result = subprocess.run(
            ["python", str(script_path)],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        console.log(f"Error running script {script_path}: {e}", style="danger")
        raise
