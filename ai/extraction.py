from textwrap import dedent
from typing import Dict, List, Union

from ai.constants import LLM_MODEL, TEMPERATURE
from ai.enums import Sentiment
from ai.keyword_extraction import extract_keywords
from ai.llm_utils import get_completion
from ai.models import StructuredInfo
from ai.tool_definitions import STRUCTURED_INFO_EXTRACTION_TOOL

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful assistant that extracts structured information from text.",
}

STRUCTURED_INFO_EXTRACTION_PROMPT = dedent(
    """ \
    You are an expert at extracting structured information from text. Given a piece of text, your task is to extract the following information:
    1. Title: The title of the text. If the text does not have a title, return an empty string.
    2. Summary: A brief summary of the text, capturing the main points and essence of the content.
    3. Sentiment: The overall sentiment of the text. Should be one of: positive, negative, neutral.
    4. Topics: A list of main topics discussed in the text.

    Text: ```{text}```
    """
)


def _make_messages(text: str) -> List[Dict[str, str]]:
    user_message = {
        "role": "user",
        "content": STRUCTURED_INFO_EXTRACTION_PROMPT.format(text=text),
    }
    return [SYSTEM_MESSAGE, user_message]


def extract_structured_info(text: str, api_key: str) -> Union[str, StructuredInfo]:
    if not text.strip():
        return "Input text is empty"
    messages = _make_messages(text)
    try:
        _, tool_calls = get_completion(
            messages,
            api_key=api_key,
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            tools=[STRUCTURED_INFO_EXTRACTION_TOOL],
        )
    except Exception as e:
        return str(e)

    if tool_calls:
        tool_call = tool_calls[0]
        title = tool_call.arguments.get("title", "")
        summary = tool_call.arguments.get("summary", "")
        sentiment_str = tool_call.arguments.get("sentiment", "")
        topics: List[str] = tool_call.arguments.get("topics", [])  # type: ignore

        sentiment = Sentiment.__members__.get(sentiment_str.lower())
    else:
        return "Failed to extract structured information"

    keywords = extract_keywords(text)

    structured_info = StructuredInfo(
        title=title,
        summary=summary,
        sentiment=sentiment,
        topics=topics,
        keywords=keywords,
    )
    structured_info.save()
    return structured_info
