from llm_parse_json import parse_json

if __name__ == '__main__':
    json_str = '{"name": "John",\n "age": 30, "city": "New York", "control_char": "\x01\x02\x7F"}'
    # cleaned_str = remove_control_characters(json_str)
    # print(cleaned_str)
    res = parse_json(json_str)
    print(res)
