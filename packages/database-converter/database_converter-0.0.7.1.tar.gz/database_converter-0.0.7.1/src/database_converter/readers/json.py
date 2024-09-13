import json


from database_converter.utils.utils import conversion_from_reading


def load_dict_from_json(json_obj) -> dict[str, any]:
    """
    Function to convert the JSON structure read in a file since a decoding needs to be done.
    By decoding, I mean that there is a need to cast the values read in their right type.
    :param json_obj: JSON structure read in a file
    :return: Decoded dictionary read in a file
    """
    decoded_json: dict[str, any] = {}
    for db_name, db in json_obj.items():
        decoded_db = {}
        for table_name, table in db.items():
            decoded_table = []
            for row in table:
                decoded_row = {}

                for col_key, col_value in row.items():
                    val = col_value.get('value')
                    typ = col_value.get('type')

                    decoded_row[col_key] = conversion_from_reading(val, typ)

                decoded_table.append(decoded_row)
            decoded_db[table_name] = decoded_table

        decoded_json[db_name] = decoded_db

    return decoded_json


def read(source_file: str) -> dict[str, any]:
    """
    Function to read the content of a converted database in a JSON file.
    :param source_file: file path
    :return: Decoded dictionary read in a file
    """
    with open(source_file, 'r') as f:
        data = json.load(f)
        decoded_data = load_dict_from_json(data)

    return decoded_data
