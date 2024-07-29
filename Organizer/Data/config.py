import configparser as cp
import json


def read(section, var):            # Чтение из 1 строчки
    config = cp.ConfigParser()
    config.read('Data/Settings/settings.ini')
    return config[f"{section}"][f"{var}"]


def read_section(section) -> dict:
    config = cp.ConfigParser()
    config.read('Data/Settings/settings.ini')
    section_dict = {}
    for item in config[section].items():
        section_dict.update({item[0]: item[1]})
    return section_dict


def read_all_config() -> dict:
    config = cp.ConfigParser()
    config.read('Data/Settings/settings.ini')
    section_dict = {}
    for section in config.sections():
        for item in config[section].items():
            section_dict.update({item[0]: item[1]})
    return section_dict


def write(section, var, value):           # Запись в 1 строчку
    config = cp.ConfigParser()
    config.read('Data/Settings/settings.ini')
    config[f"{section}"][f"{var}"] = value
    with open('Data/Settings/settings.ini', 'w') as configfile:
        config.write(configfile)


def write_json_log(value):   # Запись в файл джейсон
    with open("Data/Settings/file_log.json", "w") as write_file:
        json.dump(value, write_file, indent=4, ensure_ascii=False, sort_keys=True)


def read_json_book_lib() -> dict:
    with open("Data/Settings/book_lib.json", "r") as file:
        return json.load(file)


def read_json_orders_log() -> dict:
    with open("Data/Settings/file_log.json", "r") as file:
        return json.load(file)
