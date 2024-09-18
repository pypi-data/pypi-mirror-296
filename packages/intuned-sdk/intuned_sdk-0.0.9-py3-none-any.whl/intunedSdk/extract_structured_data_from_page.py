import logging
import os
import pickle
import json

from typing import Any, Dict, TypedDict, Literal, List

from openai import OpenAI
from openai import OpenAI
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from anthropic.types.tool_param import ToolParam
from anthropic import Anthropic


from functools import wraps

from playwright.async_api import Page
from diskcache import Cache  # type: ignore

from .utils.clean_html import clean_html

ModelName = Literal["openai", "anthropic"]

openai_client = OpenAI()
anthropic_client = Anthropic()

cache_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", ".extract_cache"
)

cache = Cache(cache_dir)


def disk_cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Create a key based on function arguments
        key = pickle.dumps((func.__name__, args, frozenset(kwargs.items())))

        # Try to get the result from cache
        result = cache.get(key)
        if result is not None:
            return result

        # If not in cache, call the function
        result = await func(*args, **kwargs)

        # Store the result in cache
        cache.set(key, result)

        return result

    return wrapper


extract_tool_name = "extract_entity_from_page"


class Tool(TypedDict):
    name: str
    description: str
    parameters: Dict[str, Any]


def get_tools(schema_to_be_extracted: Dict[str, Any]) -> List[Tool]:
    is_array = schema_to_be_extracted.get("type") == "array"
    formatted_schema: Any = (
        {
            "type": "object",
            "properties": {
                "extracted_data": schema_to_be_extracted,
                "number_of_entities": {
                    "type": "number",
                    "description": "The number of entities items in the text - not the overall total. Relay on the text to find this, if the number is not mentioned in the text, this should be null. For example, some lists say 'showing 5 our of 20 items' - 5 is the number of items in the list.",
                },
            },
            "required": ["extracted_data", "number_of_entities"],
            "additionalProperties": False,
        }
        if is_array
        else schema_to_be_extracted
    )

    return [
        {
            "name": extract_tool_name,
            "description": f"Extract entity mentioned in the html page. Relay on the parameters for more info.",
            "parameters": formatted_schema,
        },
        {
            "name": "no_data_found",
            "description": f"you should call this tool you are asked to extract data using {extract_tool_name} and you couldn't find any data, make this your last resort, if you are sure that there is no data in the text or images",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    ]


def get_system_prompt(prompt: str) -> str:
    return f"""You are a data analyst whose job is to extract structured data from an HTML page.
Please ensure that the data is extracted exactly as it appears in the HTML, without any additional formatting or alterations.
Extract the structured data exactly as it is in the HTML.
If you don't find a specific field just don't return the field.
{prompt}
"""


@disk_cache
async def openai_extract_structured_data_from_content(
    simplified_html: str, schema_to_be_extracted: Dict[str, Any], prompt: str = ""
) -> Dict[str, Any]:

    tools = get_tools(schema_to_be_extracted)

    tools_list: List[ChatCompletionToolParam] = [
        {
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            },
            "type": "function",
        }
        for tool in tools
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        temperature=0.0,
        max_tokens=4000,
        messages=[
            {
                "role": "system",
                "content": get_system_prompt(prompt),
            },
            {"role": "user", "content": simplified_html},
        ],
        tools=tools_list,
        tool_choice="required",
    )

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls and len(tool_calls) > 0:
        tool_call = tool_calls[0]
        if tool_call.function.name == "no_data_found":
            logging.info("No data found in the text or images")
            return {}
        elif tool_call.function.name == extract_tool_name:
            arguments = tool_call.function.arguments
            logging.info("Extracted structured data")
            extracted_data = json.loads(arguments)
            if "extracted_data" in extracted_data:
                return extracted_data["extracted_data"]
            else:
                return extracted_data
        else:
            logging.error(f"Unknown tool call: {tool_call.function.name}")
            raise ValueError(f"Unknown tool call: {tool_call.function.name}")
    else:
        logging.error("No tool calls found")
        raise ValueError("No tool calls found")


@disk_cache
async def anthropic_extract_structured_data_from_content(
    simplified_html: str, schema_to_be_extracted: Dict[str, Any], prompt: str = ""
) -> Dict[str, Any]:
    tools = get_tools(schema_to_be_extracted)
    tools_list: List[ToolParam] = [
        {
            "description": tool["description"],
            "input_schema": tool["parameters"],
            "name": tool["name"],
        }
        for tool in tools
    ]
    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4000,
        tools=tools_list,
        tool_choice={"type": "any"},
        messages=[
            {
                "role": "user",
                "content": simplified_html,
            }
        ],
    )

    if len(response.content) > 0 and response.content[0].type == "tool_use":
        tool_call = response.content[0]
        if tool_call.name == "no_data_found":
            logging.info("No data found in the text or images")
            return {}
        elif tool_call.name == extract_tool_name:
            arguments = tool_call.input
            logging.info("Extracted structured data")
            if "extracted_data" in arguments:
                return arguments["extracted_data"]
            else:
                return arguments


async def extract_structured_data_from_page(
    page: Page,
    schema_to_be_extracted: Dict[str, Any],
    prompt: str = "",
    model: ModelName = "openai",
) -> Dict[str, Any]:
    """
    Extracts structured data from a web page using a provided JSON schema.
    Args:
        page (Page): The web page to extract data from.
        schema_to_be_extracted (Dict[str, Any]): The JSON schema defining the structure of data to be extracted.

    Returns:
        Dict[str, Any]: The extracted structured data.
    """
    simplified_html = clean_html(await page.content())
    if model == "openai":
        return await openai_extract_structured_data_from_content(
            simplified_html, schema_to_be_extracted, prompt
        )
    elif model == "anthropic":
        return await anthropic_extract_structured_data_from_content(
            simplified_html, schema_to_be_extracted, prompt
        )
    else:
        raise ValueError(f"Unknown model: {model}")
