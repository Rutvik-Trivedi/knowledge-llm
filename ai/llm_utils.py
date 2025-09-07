import json
from typing import Any, Dict, List, Optional, Tuple

import openai
from jsonschema import ValidationError, validate
from openai import OpenAI

from ai import constants
from ai.exceptions import InvalidToolCallResponse, LLMCompletionError

MAX_COMPLETION_TRIES = 3


class ToolCall:
    def __init__(
        self,
        arguments: dict[str, str],
        tool_call_schema: Optional[dict[str, Any]] = None,
    ):
        self.tool_call_schema = tool_call_schema
        try:
            self.arguments = arguments
            if tool_call_schema is not None:
                validate(self.arguments, tool_call_schema["function"]["parameters"])
        except (json.JSONDecodeError, KeyError) as e:
            raise InvalidToolCallResponse(
                f"Invalid tool call response received. Response: {self.arguments}, Error: {e}"
            )
        except ValidationError as e:
            raise InvalidToolCallResponse(
                f"Tool call response does not match expected schema. Response: {self.arguments}, Error: {e}"
            )


def get_completion(
    messages: List[Dict[str, str]],
    api_key: str,
    model: str = constants.LLM_MODEL,
    temperature: float = 1.0,
    tools: Optional[List[dict[str, Any]]] = None,
) -> Tuple[str, List[ToolCall]]:
    if not api_key:
        raise ValueError("API key is required to get completion from LLM.")
    llm = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    for _ in range(MAX_COMPLETION_TRIES):
        try:
            response = llm.chat.completions.create(
                model=model,
                messages=messages,  # type: ignore
                temperature=temperature,
                tools=tools,  # type: ignore
            )
        except Exception as e:
            print(f"Failed to get completion from LLM API. Error: {e}")
            continue

        model_dump = response.choices[0].model_dump()
        response_message = model_dump["message"]["content"]
        tool_calls = []
        if model_dump["message"]["tool_calls"] and tools:
            for tool_response in model_dump["message"]["tool_calls"]:
                tool_name = tool_response["function"]["name"]
                tool_schema = next(
                    (tool for tool in tools if tool["function"]["name"] == tool_name),
                    None,
                )
                if tool_schema is None:
                    raise InvalidToolCallResponse(
                        f"Received tool call for unknown tool: {tool_name}"
                    )
                try:
                    tool_call = ToolCall(
                        arguments=json.loads(tool_response["function"]["arguments"]),
                        tool_call_schema=tool_schema,
                    )
                    tool_calls.append(tool_call)
                except InvalidToolCallResponse as e:
                    print(f"Invalid tool call response: {e}")
                    continue
        if response_message or tool_calls:
            return response_message, tool_calls

    raise LLMCompletionError("Failed to get a valid completion after multiple tries.")
