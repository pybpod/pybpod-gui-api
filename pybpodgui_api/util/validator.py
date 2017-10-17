# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" pycontrolapi.util.validator

"""

import re


def validate_simple_field(field_value):
    """
    Do not allow strings with spaces, latin characters and symbols (except for underscore)
    :param field_value:
    :type field_value:
    """
    if field_value is None:
        return False

    field_filter = re.compile('(^[a-zA-Z_0-9]{1,}$)')

    match = re.match(field_filter, field_value)

    return match is not None

def validate_file_name(field_value):
    """
    Do not allow strings with spaces, latin characters and symbols (except for underscore)
    File must end with .py
    :param field_value:
    :type field_value:
    """
    if field_value is None:
        return False

    field_filter = re.compile('([a-zA-Z_0-9]{1,}\.py)')

    match = re.match(field_filter, field_value)

    return match is not None

if __name__ == "__main__":
    print(validate_simple_field("setup1"))
    print(validate_simple_field("setup 1"))
    print(validate_simple_field("set?"))
    print(validate_simple_field("set!"))
    print(validate_simple_field("set@up1"))
    print(validate_simple_field("        "))
    print(validate_simple_field("sétup1"))
    print(validate_simple_field("éãê"))
