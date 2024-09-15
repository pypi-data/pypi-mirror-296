from typing import Any
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
                d[key] = {} if not path_keys[i+1].isdigit() else []
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
    
        