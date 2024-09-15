from typing import Any, List
import json



def set_value_by_path(d: dict, path: str, value: Any) -> dict:
    """
    Set a value in a nested dictionary using a dotted path.
    """
    path_keys = path.split(".")
    for i, key in enumerate(path_keys[:-1]):
        if key.isdigit():
            key = int(key)
            if not isinstance(d, list):
                d = []
            while len(d) <= key:
                d.append({})
            d = d[key]
        else:
            if key not in d:
                d[key] = {} if not path_keys[i + 1].isdigit() else []
            d = d[key]

    last_key = path_keys[-1]
    if last_key.isdigit():
        last_key = int(last_key)
        if not isinstance(d, list):
            d = []
        while len(d) <= last_key:
            d.append(None)
    d[last_key] = value


def get_value_by_path(data: dict, path: str) -> Any:
    """
    Get a value in a nested dictionary using a dotted path.
    """
    keys = path.split(".")
    for key in keys:
        if key.isdigit():
            key = int(key)
            if isinstance(data, list):
                while len(data) <= key:
                    data.append({})
                data = data[key]
        else:
            if key not in data:
                return None
            data = data[key]
    return data


def delete_value_by_path(data: dict, path: str) -> dict:
    """
    Delete a value in a nested dictionary using a dotted path.
    """
    keys = path.split(".")
    for key in keys[:-1]:
        if key.isdigit():
            key = int(key)
            if isinstance(data, list):
                while len(data) <= key:
                    data.append({})
                data = data[key]
        else:
            if key not in data:
                return data
            data = data[key]
    del data[keys[-1]]
    return data


def convert_attr_list_to_dict(attrs: list[dict]) -> dict:
    """
    OpenTelemetry attributes are stored as a list of dictionaries. This function converts the list to a nested dictionary.
    Input:
    [
        {"key": "a.0", "value": {"int_value": 1} },
        {"key": "b.c", "value": {"int_value": 2} },
        {"key": "d", "value": {"int_value": 3} },
    ]
    Output:
    {
        "a": [1],
        "b": {"c": 2},
        "d": 3,
    """
    result = {}
    try:
        for item in attrs:
            key = item["key"]
            value = next(iter(item["value"].values()))
            set_value_by_path(result, key, value)
        return result
    except Exception as e:
        raise Exception(f"Error converting attributes to dictionary: {e}")


# ===============================LLM types================================
from keywordsai_sdk.keywordsai_types._internal_types import (
    AnthropicMessage,
    AnthropicParams,
    AnthropicTool,
    AnthropicStreamChunk,
    Message,
    TextContent,
    ImageContent,
    ImageURL,
    ToolCall,
    ToolCallFunction,
    ToolChoice,
    ToolChoiceFunction,
    FunctionTool,
    FunctionParameters,
    Function,
    LLMParams,
    Properties
)

def anthropic_message_to_llm_message(message: AnthropicMessage) -> Message:
    content = message.content
    if isinstance(content, str):
        return Message(role=message.role, content=content)
    elif isinstance(content, list):
        content_list = []
        for item in content:
            if item.type == "text":
                content_list.append(TextContent(type="text", text=item.text))
            elif item.type == "image":
                content_list.append(
                    ImageContent(
                        type="image_url", image_url=ImageURL(url=item.source.data)
                    )
                )
        return Message(role=message.role, content=content_list)
    return Message(role=message.role)


def anthropic_messages_to_llm_messages(
    messages: List[AnthropicMessage],
) -> List[Message]:
    messages_to_return = []
    for message in messages:
        content = message.content
        if isinstance(content, str):
            messages_to_return.append(Message(role=message.role, content=content))
        elif isinstance(content, list):
            content_list = []
            tool_calls = []
            for item in content:
                if item.type == "text":
                    content_list.append(TextContent(type="text", text=item.text))
                elif item.type == "image":
                    content_list.append(
                        ImageContent(
                            type="image_url", image_url=ImageURL(url=item.source.data)
                        )
                    )
                elif item.type == "tool_use":
                    tool_calls.append(
                        ToolCall(
                            id=item.id,
                            function=ToolCallFunction(
                                name=item.name, arguments=item.input
                            ),
                        )
                    )
                elif item.type == "tool_result":
                    messages_to_return.append(
                        Message(
                            role="tool",
                            content=item.content,
                            tool_call_id=item.tool_use_id,
                        )
                    )
            if content_list:
                message = Message(role=message.role, content=content_list)
                if tool_calls:
                    message.tool_calls = tool_calls
                messages_to_return.append(message)
    return messages_to_return


def anthropic_tool_to_llm_tool(tool: AnthropicTool) -> FunctionTool:
    properties = {}
    required = []
    for key, value in tool.input_schema.properties.items():
        properties[key] = Properties(type=value.type, description=value.description)
        if key in tool.input_schema.required:
            required.append(key)
    function_parameters = FunctionParameters(
        type="object", properties=properties, required=required
    )
    function = Function(
        name=tool.name, description=tool.description, parameters=function_parameters
    )
    return FunctionTool(type="function", function=function)


def anthropic_params_to_llm_params(params: AnthropicParams) -> LLMParams:
    messages = anthropic_messages_to_llm_messages(
        params.messages
    )  # They have same structure
    tools = None
    tool_choice = None
    keywordsai_params = {}
    if params.tools:
        tools = [anthropic_tool_to_llm_tool(tool) for tool in params.tools]
    if params.tool_choice:
        anthropic_tool_choice = params.tool_choice
        if anthropic_tool_choice.type == "auto":
            tool_choice = "auto"
        elif anthropic_tool_choice.type == "any":
            tool_choice = "required"
        else:
            tool_choice = ToolChoice(
                type=params.tool_choice.type,
                function=ToolChoiceFunction(
                    name=getattr(params.tool_choice, "name", "")
                ),
            )
    if params.system:
        messages.insert(0, Message(role="system", content=params.system))
    if params.metadata:
        keywordsai_params: dict = params.metadata.pop("keywordsai_params", {})
        metadata_in_keywordsai_params = keywordsai_params.pop(
            "metadata", {}
        )  # To avoid conflict of kwargs
        params.metadata.update(metadata_in_keywordsai_params)
        print(params.metadata)

    llm_params = LLMParams(
        messages=messages,
        model=params.model,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        stop=params.stop_sequence,
        stream=params.stream,
        tools=tools,
        tool_choice=tool_choice,
        top_k=params.top_k,
        top_p=params.top_p,
        metadata=params.metadata,
        **keywordsai_params,
    )
    return llm_params

def anthropic_stream_chunk_to_sse(chunk: AnthropicStreamChunk) -> str:
    first_line = f"event: {chunk.type}\n"
    second_line = f"data: {json.dumps(chunk.model_dump())}\n\n"
    return first_line + second_line

# ===============================End of LLM types================================
