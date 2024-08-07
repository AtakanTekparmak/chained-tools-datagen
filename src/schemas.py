from __future__ import annotations
from pydantic import BaseModel
from typing import Union, Optional, List

from easy_fnc.schemas import (
    FunctionReturn,
    FunctionParameter,
    FunctionMetadata,
)

from easy_fnc.schemas import ModelResponse as ChainedFNCResponse

from tiny_fnc_engine import FunctionCall

class Parameter(BaseModel):
    name: str
    type: str

class Return(BaseModel):
    name: str
    type: str

class FunctionSchema(BaseModel):
    name: str
    description: str
    parameters: List[Parameter]
    required: List[str]
    returns: List[Return]

    @classmethod
    def from_dict(cls, function_schema: dict[str, any]) -> 'FunctionSchema':
        """Create a FunctionSchema object from a dictionary"""
        return cls(
            name=function_schema["name"],
            description=function_schema["description"],
            parameters=[Parameter(**p) for p in function_schema["parameters"]],
            required=function_schema["required"],
            returns=[Return(**r) for r in function_schema["returns"]]
        )
    
class UserQuery(BaseModel):
    """
    Pydantic model for user query
    """
    query: str
    available_functions: list[str]

    @classmethod
    def from_dict(cls, user_query: dict[str, any]) -> 'UserQuery':
        """Create a UserQuery object from a dictionary"""
        return cls(
            query=user_query["user_query"],
            available_functions=user_query["available_functions"]
        )

class CurriculumRow(BaseModel):
    """
    Pydantic model for a curriculum row
    """
    category: str
    subcategory: str
    task: str

    @classmethod
    def from_dict(cls, row: dict[str, any]) -> 'CurriculumRow':
        """Create a CurriculumRow object from a dictionary"""
        return cls(category=row["category"], subcategory=row["subcategory"], task=row["task"])
    
Curriculum = dict[str, list[CurriculumRow]]

class DummyReturn(BaseModel):
    """
    Pydantic model for a dummy return
    """
    value: Union[str, int, float, bool, list, dict]
    type: str

class DummyFunction(BaseModel):
    """
    Pydantic model for a dummy function
    """
    name: str
    returns: DummyReturn
    implementation: str

class FunctionCallingResponse(BaseModel):
    """
    Pydantic model for function calling response
    """
    thoughts: str
    function_calls: list[FunctionCall]

class FunctionsMetadata(BaseModel):
    """
    Pydantic model for functions metadata
    """
    functions_metadata: list[FunctionMetadata]

    @classmethod
    def from_list(cls, functions_metadata: list[FunctionMetadata]) -> 'FunctionsMetadata':
        """Create a FunctionsMetadata object from a list of FunctionMetadata objects"""
        return cls(functions_metadata=functions_metadata)

class UserMessage(BaseModel):
    """
    Pydantic model for user message
    """
    role: str = "user"
    content: Optional[str]

class SystemMessage(BaseModel):
    """
    Pydantic model for system message
    """
    role: str = "system"
    content: Optional[str]

class AssistantMessage(BaseModel):
    """
    Pydantic model for assistant message
    """
    role: str = "assistant"
    content: Optional[Union[str, FunctionCallingResponse]]

class Conversation(BaseModel):
    """
    Pydantic model for conversation
    """
    system_prompt: Optional[str]
    messages: Optional[list[Optional[Union[SystemMessage, UserMessage, AssistantMessage]]]]

    def add_user_message(self, content: Union[str, UserMessage]):
        """Add a user message to the conversation"""
        if isinstance(content, str):
            self.messages.append(UserMessage(content=content))
        else:
            self.messages.append(content)

    def add_assistant_message(self, content: Union[str, AssistantMessage]):
        """Add an assistant message to the conversation"""
        if isinstance(content, str):
            self.messages.append(AssistantMessage(content=content))
        else:
            self.messages.append(content)