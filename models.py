"""Pydantic models for function definitions and call results."""
from typing import Dict, Literal
from pydantic import BaseModel


class ParameterSchema(BaseModel):
    """Schema for a single function parameter.

    Attributes
    ----------
    type : Literal["number", "string", "boolean"]
        The expected type of the parameter.
    """

    type: Literal["number", "integer", "string", "boolean"]


class ReturnSchema(BaseModel):
    """Schema for a function's return type.

    Attributes
    ----------
    type : Literal["number", "string", "boolean"]
        The type of value the function returns.
    """

    type: Literal["number", "integer", "string", "boolean"]


class FunctionDefinition(BaseModel):
    """Definition of a callable function available to the LLM.

    Attributes
    ----------
    name : str
        The function's identifier.
    description : str
        A natural-language description of what the function does.
    parameters : Dict[str, ParameterSchema]
        Mapping of parameter names to their type schemas.
    returns : ReturnSchema
        The function's return type schema.
    """

    name: str
    description: str
    parameters: Dict[str, ParameterSchema]
    returns: ReturnSchema


class PromptItem(BaseModel):
    """A single natural-language prompt to process.

    Attributes
    ----------
    prompt : str
        The natural-language request.
    """

    prompt: str


class FunctionCallResult(BaseModel):
    """The structured function call extracted from a prompt.

    Attributes
    ----------
    prompt : str
        The original natural-language request.
    name : str
        The name of the function selected.
    parameters : Dict[str, object]
        The extracted arguments with correct types.
    """

    prompt: str
    name: str
    parameters: Dict[str, object]
