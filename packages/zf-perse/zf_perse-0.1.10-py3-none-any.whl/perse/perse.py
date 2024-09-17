import json
import os
from typing import Any, Dict, List, Type, Union

from loguru import logger
from openai import OpenAI
from pydantic import BaseModel, create_model

client = OpenAI(api_key=os.getenv("PERSE_OPENAI_API_KEY"))
model = "gpt-4o-mini-2024-07-18"

class FieldInfo(BaseModel):
    name: str
    type: str
    nested_fields: Union[List["FieldInfo"], None] = None


FieldInfo.model_rebuild()


class FieldsInfo(BaseModel):
    fields: List[FieldInfo]


def get_fields_info(content: str) -> FieldsInfo:
    if not content:
        raise ValueError("HTML content is empty")

    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """
                You are an expert at analyzing data. I will give you the contents of an HTML page and your goal is to come up with a list of field names and their data types, including nested structures. When selecting which fields to include, consider the following:
                - No markup or HTML tags or attributes should be included
                - For ul, ol, li tags, the data should be put into a list
                - For tables, the data should be put into a list of lists
                - Create nested structures when appropriate (e.g., for repeated elements or logical groupings)
                - Only lowest level text should be included as primitive data types
                - For images or videos, extract the url and choose a key based on context
                - List of object with single key-value pair should be simplified to a single list
                - No need to include html tags like svgs, canvas, etc.
                - For the type of data, always use a valid JSON data type (string, number, boolean, array, object)
                - Form forms, never include any styling, only the list of field names
                """,
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        response_format=FieldsInfo,
    )

    result_str = response.choices[0].message.content
    result = json.loads(result_str)

    fields_info = FieldsInfo(**result)
    # logger.info(f"FieldsInfo: {fields_info}")
    return fields_info


def generate_pydantic_model(fields_info: List[FieldInfo]) -> Type[BaseModel]:
    TYPE_MAPPING: Dict[str, Any] = {
        "string": str,
        "number": float,
        "boolean": bool,
        "array": List[Any],
        "object": Dict[str, Any],
    }

    fields_dict: Dict[str, Any] = {}

    for field in fields_info:
        if field.nested_fields:
            nested_model = generate_pydantic_model(field.nested_fields)
            if field.type.lower() == "array":
                fields_dict[field.name] = (List[nested_model], ...)
            else:
                fields_dict[field.name] = (nested_model, ...)
        else:
            fields_dict[field.name] = (TYPE_MAPPING.get(field.type.lower(), Any), ...)

    return create_model("GeneratedModel", **fields_dict)


def recursive_dump(model: BaseModel) -> Dict[str, Any]:
    def _dump(obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return {k: _dump(v) for k, v in obj.model_dump().items()}
        elif isinstance(obj, list):
            return [_dump(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: _dump(v) for k, v in obj.items()}
        else:
            return obj

    return _dump(model)


def extract_json_fields(content: str, GeneratedModel: BaseModel) -> Dict[str, Any]:
    if not content:
        raise ValueError("HTML content is empty")

    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """
                You are given the contents of an HTML page. Your goal is to extract useful information from the page and fill the given DataObject type. The extracted should satisfy the following criteria:
                - No markup or HTML tags or attributes should be included
                - For ul, ol, li tags, the data should be put into JSON list
                - For tables, the data should be put into JSON list of lists
                - For all other tags, the data should be put into JSON dictionary
                - Only lowest level text should be included as primitive data types
                - For images or videos, extract the url and choose a key based on context
                - No need to include html tags like svgs, canvas, etc.
                """,
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        response_format=GeneratedModel,
    )

    result_str = response.choices[0].message.content
    result = json.loads(result_str)

    json_data = GeneratedModel(**result)
    # logger.info(f"Parsed Data: {json_data}")
    return recursive_dump(json_data)


def perse(content: str) -> Dict[str, Any]:
    fields_info = get_fields_info(content)
    fields = fields_info.fields
    logger.debug(f"Identified {len(fields)} top-level fields: {', '.join([f.name for f in fields])}")
    GeneratedModel = generate_pydantic_model(fields_info.fields)
    logger.debug("Successfully generated strictly typed data model")
    if not GeneratedModel:
        raise ValueError("Could not build data model")
    logger.debug(f"Now performing data extraction using {model}")
    return extract_json_fields(content, GeneratedModel)


def perse_str(content: str) -> str:
    return json.dumps(perse(content), indent=2)


if __name__ == "__main__":
    print(perse_str(open("./tests/input.html", "r", encoding="utf-8").read()))
