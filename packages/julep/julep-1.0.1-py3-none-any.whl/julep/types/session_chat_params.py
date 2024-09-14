# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .message_param import MessageParam

__all__ = [
    "SessionChatParams",
    "ResponseFormat",
    "ResponseFormatSimpleCompletionResponseFormat",
    "ResponseFormatSchemaCompletionResponseFormat",
    "ToolChoice",
    "ToolChoiceNamedFunctionChoice",
    "ToolChoiceNamedFunctionChoiceFunction",
    "ToolChoiceNamedIntegrationChoice",
    "ToolChoiceNamedSystemChoice",
    "ToolChoiceNamedAPICallChoice",
    "Tool",
    "ToolFunction",
]


class SessionChatParams(TypedDict, total=False):
    messages: Required[Iterable[MessageParam]]

    agent: Optional[str]

    frequency_penalty: Optional[float]

    length_penalty: Optional[float]

    logit_bias: Optional[Dict[str, float]]

    max_tokens: Optional[int]

    min_p: Optional[float]

    model: Optional[str]

    presence_penalty: Optional[float]

    recall: bool

    repetition_penalty: Optional[float]

    response_format: Optional[ResponseFormat]

    save: bool

    seed: Optional[int]

    stop: List[str]

    stream: bool

    temperature: Optional[float]

    tool_choice: Optional[ToolChoice]

    tools: Iterable[Tool]

    top_p: Optional[float]


class ResponseFormatSimpleCompletionResponseFormat(TypedDict, total=False):
    type: Literal["text", "json_object"]


class ResponseFormatSchemaCompletionResponseFormat(TypedDict, total=False):
    json_schema: Required[object]

    type: Literal["json_schema"]


ResponseFormat: TypeAlias = Union[
    ResponseFormatSimpleCompletionResponseFormat, ResponseFormatSchemaCompletionResponseFormat
]


class ToolChoiceNamedFunctionChoiceFunction(TypedDict, total=False):
    name: Required[str]


class ToolChoiceNamedFunctionChoice(TypedDict, total=False):
    function: Required[ToolChoiceNamedFunctionChoiceFunction]


class ToolChoiceNamedIntegrationChoice(TypedDict, total=False):
    integration: Optional[object]


class ToolChoiceNamedSystemChoice(TypedDict, total=False):
    system: Optional[object]


class ToolChoiceNamedAPICallChoice(TypedDict, total=False):
    api_call: Optional[object]


ToolChoice: TypeAlias = Union[
    Literal["auto", "none"],
    ToolChoiceNamedFunctionChoice,
    ToolChoiceNamedIntegrationChoice,
    ToolChoiceNamedSystemChoice,
    ToolChoiceNamedAPICallChoice,
]


class ToolFunction(TypedDict, total=False):
    description: Optional[str]

    name: Optional[object]

    parameters: Optional[object]


class Tool(TypedDict, total=False):
    function: Required[ToolFunction]
    """Function definition"""

    name: Required[str]

    api_call: Optional[object]

    integration: Optional[object]

    system: Optional[object]

    type: Literal["function", "integration", "system", "api_call"]
