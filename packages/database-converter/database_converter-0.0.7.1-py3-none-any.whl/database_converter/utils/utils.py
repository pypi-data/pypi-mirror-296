import itertools
import os
import re
import sys


import database_converter.utils.constants as constants


def dict_factory(cursor, row):
    """
    Function to return a row as a python dictionary
    :param cursor: a sqlite3 cursor object
    :param row: a row
    :return: a python dictionary
    """
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


all_chars = (chr(i) for i in range(sys.maxunicode))
categories = {'Cc', 'Cf', 'Cs', 'Co', 'Cn'}
control_chars = ''.join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))
control_chars_bytes = bytes(control_chars.encode('utf-8'))
control_char_re = re.compile('[%s]' % re.escape(control_chars))


def remove_control_chars(s: str) -> str:
    return control_char_re.sub('', s)


def remove_control_chars_and_split_bytes(b: bytes) -> list:
    """Splits the bytes object by control characters and returns a list of bytes chunks."""
    result = []
    current_chunk = []

    for byte in b:
        if byte in control_chars_bytes:
            # If we hit a control character and have a current chunk, store it
            if current_chunk:
                result.append(bytes(current_chunk))
                current_chunk = []
        else:
            # Append non-control characters to the current chunk
            current_chunk.append(byte)

    # Append any remaining chunk after the loop
    if current_chunk:
        result.append(bytes(current_chunk))

    return result


def remove_orphans_from_bytes(item: bytes, minimal_length: int = 3) -> bytes:
    pass


def winapi_path(dos_path):
    """
    Function to add the windows path extension to allow longer paths
    :param dos_path: the base path
    :return: a string of a path
    """
    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path


def convert_multidimensional_to_single_dimensional(values: any, elem_key: str = "") -> dict[str, any]:
    """
    Recursive function to convert a multidimensional python dictionary to a single dimensional python dictionary
    :param values: an object of any type
    :param elem_key: the key associated with the parameter values
    :return: a single dimensional python dictionary
    """
    # a single dimensional row
    one_dimension_row: dict[str, any] = {}

    if isinstance(values, dict):
        # go through every key of the dictionary
        for key_elem, elem in values.items():
            sub_key = f"{elem_key} {constants.SEP_KEY_CHAR} {key_elem}" if elem_key else f"{key_elem}"
            one_dimension_row |= convert_multidimensional_to_single_dimensional(values=elem, elem_key=sub_key)
    elif isinstance(values, list) or isinstance(values, tuple):
        # go through every index of the list
        for index_elem, elem in enumerate(values):
            sub_key = f"{elem_key} {constants.SEP_KEY_CHAR} {index_elem}" if elem_key else f"{index_elem}"
            one_dimension_row |= convert_multidimensional_to_single_dimensional(values=elem, elem_key=sub_key)
    else:
        # simply add the values parameter to the key
        one_dimension_row |= {elem_key: values}

    return one_dimension_row


def check_file_type(filepath: str, filetype: str) -> bool:
    header = b''

    if constants.FILE_HEADERS.get(filetype, None):
        expected_header, header_length = constants.FILE_HEADERS.get(filetype)

        try:
            with open(filepath, 'rb') as f:
                header = f.read(header_length)
        except PermissionError as e:
            print(f"Permission denied with error {e}")

        return header == expected_header

    return False


def conversion_for_writing(value: any) -> dict:
    """
    Function to convert a value into its written format. When storing a data in a structured file where bytes can't be
    written and numbers are written as strings, this function is used.
    :param value: the value to be converted
    :return: the converted value
    """
    typ = type(value).__name__

    if isinstance(value, bytes):
        val = value.hex()
    else:
        val = remove_control_chars(str(value))
    return {'value': val, 'type': typ}


def conversion_from_reading(val: str, typ: str) -> any:
    """
    Function to cast properly a string element based on a given type
    :param val: the value to be converted
    :param typ: the real type of the value
    :return: the casted value
    """
    new_val: any = val
    if typ == 'int':
        new_val = int(val)
    elif typ == 'float':
        new_val = float(val)
    elif typ == 'bytes':
        new_val = bytes.fromhex(val)
    elif typ == 'NoneType':
        new_val = None

    return new_val
