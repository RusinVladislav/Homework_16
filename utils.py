import json


def load_data(filename: str) -> json:
    """
    загружает сырые данные из файла json
    :param filename: str
    :return: json
    """
    with open(filename, 'r', encoding='UTF8') as file:
        return json.load(file)
