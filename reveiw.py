import os
import logging

import dotenv
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.markdown import Markdown


logging.basicConfig(
    level=logging.WARN, format="%(asctime)s - %(levelname)s - %(message)s"
)

dotenv.load_dotenv()

MODEL = os.getenv("MODEL")
LANGUAGE = os.getenv("LANGUAGE") or "KOREAN"

console = Console()


def main():
    llm = ChatOpenAI(model=MODEL)

    content = get_content()

    review = get_review(llm, content, LANGUAGE)

    formatted_review = format_review(review)

    console.print(formatted_review)


def get_content():
    with open("local/commits.json", "r") as f:
        content = f.read()
        logging.debug(content)

    return content


def get_review(llm: ChatOpenAI, content: str, language: str) -> str:
    review = llm.invoke(
        [
            (
                "assistant",
                f"Review the user's git commits,  OUTPUT THE REVIEW IN {language}.",
            ),
            ("human", content),
        ]
    ).content

    review = str(review)

    return review


def format_review(review: str):
    diff_syntax = Markdown(review, code_theme="ansi_dark")

    return diff_syntax


if __name__ == "__main__":
    main()
