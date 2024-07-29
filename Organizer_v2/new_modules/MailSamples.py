import os


class MailSamples:
    """Класс для обработки файлов текстовых шаблонов"""
    __slots__ = '__ms_list'
    __INSTANCE = None
    SAMPLE = []

    def __new__(cls, *args, **kwargs):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE

    def __init__(self):
        self.__ms_list = tuple(x for x in os.listdir('data/MailSamples') if x != '__readme.txt')

    def get_ms_list(self) -> tuple:
        """Возвращает кортеж из значенией списка текстовых шаблонов"""
        return tuple(x[:-4] for x in self.__ms_list)

    def create_sample(self, index: int):
        """Разбивает строки на части по литералу ?%"""
        with open(f'data/MailSamples/{self.__ms_list[index]}', 'r', encoding='UTF-8') as txt_file:
            self.SAMPLE.clear()
            self.SAMPLE.extend(txt_file.read().split('?%'))
