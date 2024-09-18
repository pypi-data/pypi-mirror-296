import json

from llm_parse_json import parse_json
import re

from llm_parse_json.parser import _preprocess_json_string, _extract_json_frame

json_str = 'jasjfja{"name": "John",\n "age": 30, "city": "\\nNew \nYork", "address": {"street": "123 Main St", "zip": "10001"}}'
res = parse_json(json_str)
print(type(res))
print(res)
json_array_str = 'asjdfjlkaj[{"\\nname": "\nJohn"}, {"name": "Jane"}]'
res = parse_json(json_array_str)
print(type(res))
print(res)



def remove_control_characters(json_str):
    """
    移除 JSON 字符串中的所有控制字符和删除字符，但保留换行符和回车符。
    """
    cleaned_response_str = re.sub(r'[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]', '', json_str)
    return cleaned_response_str
def parse_json(json_str):
    """
    解析 JSON 字符串，根据其格式选择使用解析对象或数组的方法。
    """
    json_frame = _extract_json_frame(json_str)
    print(f"提取的 JSON 框架: {json_frame}")

    cleaned_response_str = re.sub(r'[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]', '', json_frame)
    print(f"移除控制字符后的字符串: {cleaned_response_str}")

    json_data = _preprocess_json_string(cleaned_response_str)
    print(f"预处理后的 JSON 字符串: {json_data}")

    return json.loads(json_data)
if __name__ == '__main__':
    json_str = '{"name": "John",\n "age": 30, "city": "New York", "control_char": "\x01\x02\x7F"}'
    cleaned_str = remove_control_characters(json_str)
    print(cleaned_str)
    res = parse_json(json_str)
