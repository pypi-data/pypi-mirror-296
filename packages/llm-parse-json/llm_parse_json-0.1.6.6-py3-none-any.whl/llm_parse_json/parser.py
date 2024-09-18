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
    result = []

    for char in json_str:
        if char == '"':
            in_string = not in_string
        if char == '\n' and in_string:
            result.append('\\n')
        else:
            result.append(char)

    escaped_str = ''.join(result)
    logging.debug(f"转义后的 JSON 字符串: {escaped_str}")
    return escaped_str


def _preprocess_json_string(json_str):
    """
    预处理 JSON 字符串，转义值中的换行符并移除多余空白字符。
    """
    logging.debug("开始预处理 JSON 字符串")

    json_str = _escape_newlines_in_json_value(json_str)

    # 移除键值对之间的多余空白字符
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

    # 查找 JSON 对象或数组的开头
    first_brace_index = json_str.find('{')
    first_bracket_index = json_str.find('[')

    if first_brace_index == -1 and first_bracket_index == -1:
        logging.error("无效的 JSON 输入")
        raise ValueError("Invalid JSON input")

    if first_brace_index != -1 and (first_bracket_index == -1 or first_brace_index < first_bracket_index):
        return _extract_frame(json_str, '{', '}')
    else:
        return _extract_frame(json_str, '[', ']')


def _extract_frame(json_str, open_char, close_char):
    """
    提取指定类型（对象或数组）的 JSON 框架。
    """
    logging.debug(f"开始提取 {open_char}{close_char} 框架")
    stack = []

    for i, char in enumerate(json_str):
        if char == open_char:
            stack.append(i)
        elif char == close_char:
            start_index = stack.pop()
            if not stack:
                result = json_str[start_index:i + 1].strip()
                logging.debug(f"提取到的 JSON 框架: {result}")
                return result

    logging.error("无效的 JSON 输入")
    raise ValueError("Invalid JSON input")


def _clean_special_characters(json_str):
    """
    清理掉特殊字符，包括 JSON 字符串中转义符和不可见字符。
    """
    logging.debug("开始清理特殊字符")

    # 统一移除控制字符、不可见字符、转义字符，保留最基本的 ASCII 打印字符
    json_str = re.sub(r'[\x00-\x1F\x7F\\[bfnrtv"\\][^ -~]]', '', json_str)

    logging.debug(f"清理后的 JSON 字符串: {json_str}")
    return json_str


def parse_json(json_str):
    """
    解析 JSON 字符串，根据其格式选择使用解析对象或数组的方法。
    """
    logging.debug("开始解析 JSON 字符串")

    # 提取出 JSON 框架
    json_frame = _extract_json_frame(json_str)

    # 尝试直接解析
    try:
        return json.loads(json_frame)
    except (json.JSONDecodeError, ValueError):
        logging.warning("直接解析 JSON 失败，尝试预处理")

    # 尝试预处理后的解析（转义换行符和移除多余空白）
    try:
        preprocessed_str = _preprocess_json_string(json_frame)
        return json.loads(preprocessed_str)
    except (json.JSONDecodeError, ValueError):
        logging.warning("预处理后解析 JSON 失败，尝试移除特殊字符")

    # 尝试最后的清理特殊字符并解析
    try:
        cleaned_str = _clean_special_characters(json_frame)
        return json.loads(cleaned_str)
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"解析 JSON 失败: {e}")
        raise
