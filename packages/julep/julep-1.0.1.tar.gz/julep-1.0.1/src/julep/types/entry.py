# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "Entry",
    "Content",
    "ContentUnionMember0",
    "ContentUnionMember0Content",
    "ContentUnionMember0ContentModel",
    "ContentUnionMember0ContentModelImageURL",
    "ContentTool",
    "ContentToolFunction",
    "ContentChosenFunctionCall",
    "ContentChosenFunctionCallFunction",
    "ContentChosenIntegrationCall",
    "ContentChosenSystemCall",
    "ContentChosenAPICall",
    "ContentToolResponse",
    "ContentUnionMember8",
    "ContentUnionMember8UnionMember0",
    "ContentUnionMember8UnionMember0Content",
    "ContentUnionMember8UnionMember0ContentModel",
    "ContentUnionMember8UnionMember0ContentModelImageURL",
    "ContentUnionMember8Tool",
    "ContentUnionMember8ToolFunction",
    "ContentUnionMember8ChosenFunctionCall",
    "ContentUnionMember8ChosenFunctionCallFunction",
    "ContentUnionMember8ChosenIntegrationCall",
    "ContentUnionMember8ChosenSystemCall",
    "ContentUnionMember8ChosenAPICall",
    "ContentUnionMember8ToolResponse",
]


class ContentUnionMember0Content(BaseModel):
    text: str

    type: Optional[Literal["text"]] = None


class ContentUnionMember0ContentModelImageURL(BaseModel):
    url: str

    detail: Optional[Literal["low", "high", "auto"]] = None


class ContentUnionMember0ContentModel(BaseModel):
    image_url: ContentUnionMember0ContentModelImageURL
    """The image URL"""

    type: Optional[Literal["image_url"]] = None


ContentUnionMember0: TypeAlias = Union[ContentUnionMember0Content, ContentUnionMember0ContentModel]


class ContentToolFunction(BaseModel):
    description: Optional[str] = None

    name: Optional[object] = None

    parameters: Optional[object] = None


class ContentTool(BaseModel):
    id: str

    created_at: datetime

    function: ContentToolFunction
    """Function definition"""

    name: str

    updated_at: datetime

    api_call: Optional[object] = None

    integration: Optional[object] = None

    system: Optional[object] = None

    type: Optional[Literal["function", "integration", "system", "api_call"]] = None


class ContentChosenFunctionCallFunction(BaseModel):
    name: str


class ContentChosenFunctionCall(BaseModel):
    id: str

    function: ContentChosenFunctionCallFunction

    type: Optional[Literal["function"]] = None


class ContentChosenIntegrationCall(BaseModel):
    id: str

    integration: object

    type: Optional[Literal["integration"]] = None


class ContentChosenSystemCall(BaseModel):
    id: str

    system: object

    type: Optional[Literal["system"]] = None


class ContentChosenAPICall(BaseModel):
    id: str

    api_call: object

    type: Optional[Literal["api_call"]] = None


class ContentToolResponse(BaseModel):
    id: str

    output: object


class ContentUnionMember8UnionMember0Content(BaseModel):
    text: str

    type: Optional[Literal["text"]] = None


class ContentUnionMember8UnionMember0ContentModelImageURL(BaseModel):
    url: str

    detail: Optional[Literal["low", "high", "auto"]] = None


class ContentUnionMember8UnionMember0ContentModel(BaseModel):
    image_url: ContentUnionMember8UnionMember0ContentModelImageURL
    """The image URL"""

    type: Optional[Literal["image_url"]] = None


ContentUnionMember8UnionMember0: TypeAlias = Union[
    ContentUnionMember8UnionMember0Content, ContentUnionMember8UnionMember0ContentModel
]


class ContentUnionMember8ToolFunction(BaseModel):
    description: Optional[str] = None

    name: Optional[object] = None

    parameters: Optional[object] = None


class ContentUnionMember8Tool(BaseModel):
    id: str

    created_at: datetime

    function: ContentUnionMember8ToolFunction
    """Function definition"""

    name: str

    updated_at: datetime

    api_call: Optional[object] = None

    integration: Optional[object] = None

    system: Optional[object] = None

    type: Optional[Literal["function", "integration", "system", "api_call"]] = None


class ContentUnionMember8ChosenFunctionCallFunction(BaseModel):
    name: str


class ContentUnionMember8ChosenFunctionCall(BaseModel):
    id: str

    function: ContentUnionMember8ChosenFunctionCallFunction

    type: Optional[Literal["function"]] = None


class ContentUnionMember8ChosenIntegrationCall(BaseModel):
    id: str

    integration: object

    type: Optional[Literal["integration"]] = None


class ContentUnionMember8ChosenSystemCall(BaseModel):
    id: str

    system: object

    type: Optional[Literal["system"]] = None


class ContentUnionMember8ChosenAPICall(BaseModel):
    id: str

    api_call: object

    type: Optional[Literal["api_call"]] = None


class ContentUnionMember8ToolResponse(BaseModel):
    id: str

    output: object


ContentUnionMember8: TypeAlias = Union[
    List[ContentUnionMember8UnionMember0],
    ContentUnionMember8Tool,
    ContentUnionMember8ChosenFunctionCall,
    ContentUnionMember8ChosenIntegrationCall,
    ContentUnionMember8ChosenSystemCall,
    ContentUnionMember8ChosenAPICall,
    str,
    ContentUnionMember8ToolResponse,
]

Content: TypeAlias = Union[
    List[ContentUnionMember0],
    ContentTool,
    ContentChosenFunctionCall,
    ContentChosenIntegrationCall,
    ContentChosenSystemCall,
    ContentChosenAPICall,
    str,
    ContentToolResponse,
    List[ContentUnionMember8],
]


class Entry(BaseModel):
    id: str

    content: Content

    created_at: datetime

    role: Literal["user", "assistant", "system", "function", "function_response", "function_call", "auto"]

    source: Literal["api_request", "api_response", "tool_response", "internal", "summarizer", "meta"]

    timestamp: float

    token_count: int

    tokenizer: str

    name: Optional[str] = None
