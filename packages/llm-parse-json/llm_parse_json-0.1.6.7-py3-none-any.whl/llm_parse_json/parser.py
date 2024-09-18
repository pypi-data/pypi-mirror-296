import json
import re


def _escape_newlines_in_json_value(json_str):
    in_string = False
    result = []

    for char in json_str:
        if char == '"':
            in_string = not in_string
        if char == '\n' and in_string:
            result.append('\\n')
        else:
            result.append(char)

    return ''.join(result)


def _preprocess_json_string(json_str):
    json_str = _escape_newlines_in_json_value(json_str)
    json_str = re.sub(r'(?<=:|,)\s+', '', json_str)
    return json_str


def _extract_json_frame(json_str):
    json_str = json_str.strip()

    if not json_str:
        raise ValueError("EMPTY JSON")

    first_brace_index = json_str.find('{')
    first_bracket_index = json_str.find('[')

    if first_brace_index == -1 and first_bracket_index == -1:
        raise ValueError("Invalid JSON input")

    if first_brace_index != -1 and (first_bracket_index == -1 or first_brace_index < first_bracket_index):
        return _extract_frame(json_str, '{', '}')
    else:
        return _extract_frame(json_str, '[', ']')


def _extract_frame(json_str, open_char, close_char):
    stack = []

    for i, char in enumerate(json_str):
        if char == open_char:
            stack.append(i)
        elif char == close_char:
            start_index = stack.pop()
            if not stack:
                return json_str[start_index:i + 1].strip()

    raise ValueError("Invalid JSON input")


def _clean_special_characters(json_str):
    json_str = re.sub(r'[\x00-\x1F\x7F]', '', json_str)
    json_str = re.sub(r'\\[bfnrtv"\\]', '', json_str)
    return json_str


def parse_json(json_str):
    json_frame = _extract_json_frame(json_str)

    try:
        return json.loads(json_frame)
    except (json.JSONDecodeError, ValueError):
        pass

    try:
        preprocessed_str = _preprocess_json_string(json_frame)
        return json.loads(preprocessed_str)
    except (json.JSONDecodeError, ValueError):
        pass

    try:
        cleaned_str = _clean_special_characters(json_frame)
        return json.loads(cleaned_str)
    except (json.JSONDecodeError, ValueError) as e:
        raise
