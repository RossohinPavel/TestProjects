def write_txt(path: str, string: str) -> None:
    """
    Функция для записи текстового файла. Перезаписывает файл, если он существует
    :param path: Путь, где будет сохранен файл
    :param string: Строка с информацией
    :return: None
    """
    with open(path, 'w') as file:
        file.write(string)
