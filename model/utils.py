import re


def parse_box_office(value_string):
    """
    Parse the box office string from wikipedia
    :param value_string: the box office string
    :return: the int of value
    """

    value_string = (value_string.split('\n'))[0]  # only use the first line
    if value_string[0] != '$' and (not value_string[0].isdigit()):
        raise ValueError('The box office unit is not US dollar')

    if "," in value_string:
        # Example: 7,237,794
        value = (re.findall(r"[\d\,\d]+", value_string))[0]
        value = value.replace(",", "")
    else:
        # Example: $145.8 million
        value = (re.findall(r"\d*\.\d+|\d+", value_string))[0]
    value = float(value)
    if "million" in value_string:
        value *= 1000000  # multiply a million
    elif "billion" in value_string:
        value *= 1000000000  # multiply a billion
    return value


def get_readable_string_from_int(number):
    """
    Gets a readable number string from int
    :param number: the integer number
    :return: the human readable string of input number
    """
    if number < 1000:
        # Example: 100.0 -> 100.0
        return "$" + str(round(number, 1))
    elif number < 1000000:
        # Example: 10000.03 -> $10.0 thousand
        return "$" + str(round(number / 1000, 1)) + " thousand"
    elif number < 1000000000:
        # Example: 10000000.03 -> $10.0 million
        return "$" + str(round(number / 1000000, 1)) + " million"
    else:
        # Example: 10000000000.03 -> $10.0 billion
        return "$" + str(round(number / 1000000000, 1)) + " billion"


def parse_string_to_list(value_string):
    """
    Parse a string to list. For example, "Italy[3]\nJapan" -> ["Italy", "Japan"]
    :param value_string: the input string
    :return: a list of parsed result
    """
    value_string = (value_string.split('\n'))
    lang_list = [re.search("([a-zA-Z\s]+)", v).group(1) for v in value_string if v != ""]
    return lang_list


def select_top_k(input_list, k):
    """
    Selects the top k values from input list. If the length of input list is less than k, return input list
    :param input_list: the input list
    :param k: the threshold integer
    :return: the cropped list
    """
    if len(input_list) < k:
        return input_list
    else:
        return input_list[:k]


def select_bottom_k(input_list, k):
    """
    Selects the bottom k values from input list except for the last item.
    If the length of input list is less than k, return input list.
    :param input_list: the input list
    :param k: the threshold integer
    :return: the cropped list
    """
    if len(input_list) < (k + 1):
        return input_list
    else:
        return input_list[-(k + 1): -1]
