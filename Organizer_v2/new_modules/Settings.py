import pickle


class Settings:
    """Класс для работы с файлом настроек"""
    __instance = None
    __configs = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            with open('data/settings.pcl', 'rb') as file:
                cls.__configs.update(pickle.load(file))

        return cls.__instance

    def read(self, *args: str | list) -> object | dict:
        """Чтение данных из файла настроек.
        Значение автологгирования заказов:
         - autolog: bool
        Глубина проверки заказов:
         - log_check_depth: int
        Рабочие папки:
         - order_main_dir: str
         - fotoprint_temp_dir: str
         - roddom_main_dir: str
         Настройки для работы с файлами:
         - stroke_size: int
         - stroke_color: str
         - guideline_size: int
         - guideline_color: str
        :return: Значение ключа, если передано одно значение. Если передано много - словарь с указанными ключами и
        соответствующими значениями.
        """
        if len(args) == 1:
            return self.__configs.get(args[0])
        elif len(args) > 1:
            return {key: self.__configs[key] for key in args if key in self.__configs}

    def update(self, **kwargs):
        """Обновление данных настроек. Также перезаписывает сам файл настроек.
        Значение автологгирования заказов:
         - autolog: bool
        Глубина проверки заказов:
         - log_check_depth: int
        Рабочие папки:
         - order_main_dir: str
         - fotoprint_temp_dir: str
         - roddom_main_dir: str
         Настройки для работы с файлами:
         - stroke_size: int
         - stroke_color: str
         - guideline_size: int
         - guideline_color: str
        :param kwargs: Ключи для словаря settings и новые значения к ним.
        :return: None
        """
        for key, value in kwargs.items():
            if key in self.__configs:
                self.__configs[key] = value
        with open('data/settings.pcl', 'wb') as file:
            pickle.dump(self.__configs, file)
