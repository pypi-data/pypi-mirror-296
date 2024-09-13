import json
import re
import logging

# 配置日志，默认级别为 WARNING
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

def set_logging_level(level):
    """
    设置日志级别
    """
    logging.getLogger().setLevel(level)

def _escape_newlines_in_json_value(json_str):
    """
    将 JSON 字符串中的值中的换行符转义为 \\n。
    """
    logging.debug("开始转义 JSON 值中的换行符")
    in_string = False
    escaped_str = []
    for char in json_str:
        if char == '"':
            in_string = not in_string
        if char == '\n' and in_string:
            escaped_str.append('\\n')
        else:
            escaped_str.append(char)
    result = ''.join(escaped_str)
    logging.debug(f"转义后的 JSON 字符串: {result}")
    return result

def _preprocess_json_string(json_str):
    """
    预处理 JSON 字符串，首先转义值中的换行符，然后移除键值对间多余的空白字符。
    """
    logging.debug("开始预处理 JSON 字符串")
    # 首先转义 JSON 值中的换行符
    json_str = _escape_newlines_in_json_value(json_str)

    # 移除键值对之间的多余空白字符（例如换行符、制表符等）
    json_str = re.sub(r'(?<=:|,)\s+', '', json_str)
    logging.debug(f"预处理后的 JSON 字符串: {json_str}")

    return json_str

def _extract_json_frame(json_str):
    """
    提取 JSON 字符串中的对象或数组框架。
    """
    logging.debug("开始提取 JSON 框架")
    json_str = json_str.strip()

    if not json_str:
        logging.error("JSON 字符串为空")
        raise ValueError("EMPTY JSON")

    # 查找第一个对象或数组的起始位置
    first_brace_index = json_str.find('{')
    first_bracket_index = json_str.find('[')

    if first_brace_index == -1 and first_bracket_index == -1:
        logging.error("无效的 JSON 输入")
        raise ValueError("Invalid JSON input")

    if first_brace_index != -1 and (first_bracket_index == -1 or first_brace_index < first_bracket_index):
        return _extract_object_frame(json_str)
    else:
        return _extract_array_frame(json_str)

def _extract_object_frame(json_str):
    """
    提取 JSON 对象字符串框架。
    """
    logging.debug("开始提取 JSON 对象框架")
    stack = []
    for i, char in enumerate(json_str):
        if char == '{':
            stack.append(i)
        elif char == '}':
            start_index = stack.pop()
            if not stack:
                result = json_str[start_index:i + 1].strip()
                logging.debug(f"提取到的 JSON 对象框架: {result}")
                return result
    logging.error("无效的 JSON 输入")
    raise ValueError("Invalid JSON input")

def _extract_array_frame(json_str):
    """
    提取 JSON 数组字符串框架。
    """
    logging.debug("开始提取 JSON 数组框架")
    stack = []
    for i, char in enumerate(json_str):
        if char == '[':
            stack.append(i)
        elif char == ']':
            start_index = stack.pop()
            if not stack:
                result = json_str[start_index:i + 1].strip()
                logging.debug(f"提取到的 JSON 数组框架: {result}")
                return result
    logging.error("无效的 JSON 输入")
    raise ValueError("Invalid JSON input")

def parse_json(json_str):
    """
    解析 JSON 字符串，根据其格式选择使用解析对象或数组的方法。
    """
    logging.debug("开始解析 JSON 字符串")
    try:
        json_frame = _extract_json_frame(json_str)
    except ValueError as e:
        logging.error(f"提取 JSON 框架时出错: {e}")
        raise

    try:
        cleaned_response_str = re.sub(r'[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]', '', json_frame)
        json_data = _preprocess_json_string(cleaned_response_str)
        result = json.loads(json_data)
        logging.debug(f"最终解析的 JSON 数据: {result}")
        return result
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"解析 JSON 数据时出错: {e}")
        raise