import new_modules.Win.Source as Source
from new_modules.Win.MailSamples import MailSamplesWindow
from new_modules.Win.Settings import SettingsWindow
from new_modules.Win.Roddom import RoddomWindow
from new_modules.Win.Library import LibraryWindow

from new_modules.Settings import Settings
from new_modules.Lib.Library import Library


class Window(Source.tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_cells()
        self.show_menus()
        self.set_main_graph_settings()
        self.app_settings = Settings()
        self.app_library = Library()

    def init_cells(self):
        """Фрейм получения информации о заказе"""
        info_cell_label = Source.CellLabel(master=self, label_text='Работа с заказами', label_color='#ed95b7')
        info_cell_label.pack()
        info_cell = Source.CellTwoButton(master=self, bt_l_name='Обновить БД', bt_l_func=lambda: Log.main(),
                                         bt_r_name='СтикГен', bt_r_func=lambda: StickerGenWindow(self))
        info_cell.pack()
        """Фрейм умной обработки изображений в заказе"""
        smart_proc_label = Source.CellLabel(master=self, label_color='dark salmon', label_text='Умная обработка')
        smart_proc_label.pack()
        book_btns = Source.CellTwoButton(master=self, bt_l_name='Фотокниги', bt_l_func=lambda: SmartProcWindow(self),
                                         bt_r_name='Лайфлеты', bt_r_func=None)
        book_btns.pack()
        aj_btns = Source.CellTwoButton(master=self, bt_l_name='Альбомы', bt_l_func=None,
                                       bt_r_name='Журналы', bt_r_func=None)
        aj_btns.pack()
        canvas_btn = Source.CellOneButton(master=self, func_name='Холсты', func=None)
        canvas_btn.pack(padx=80)
        """Фрейм бакапа файлов заказа"""
        bup_label = Source.CellLabel(master=self, label_color='#adc6ed', label_text='Бакап файлов заказа')
        bup_label.pack()
        bup_button = Source.CellOneButton(master=self, func_name='Подготовка к печати', pd_x=10,
                                          func=lambda: BackUpWindow(self))
        bup_button.pack()
        """Фрейм обработки фотопечати"""
        fotoprint_label = Source.CellLabel(master=self, label_color='pale green', label_text='Фотопечать')
        fotoprint_label.pack()
        roddom_cell = Source.CellOneButton(master=self, func_name='Роддом', pd_x=50, func=lambda: RoddomWindow(self))
        roddom_cell.pack()
        """Фрейм социальных функций"""
        social_label = Source.CellLabel(master=self, label_color='#7683de', label_text='Общение', )
        social_label.pack()
        mail_sample_btn = Source.CellOneButton(master=self, func_name='Текстовые шаблоны', pd_x=10,
                                               func=lambda: MailSamplesWindow(self))
        mail_sample_btn.pack()

    def set_main_graph_settings(self):
        """Функция основных настроек окна, положения, размера и тд."""
        self.title('Органайзер 2_1 BETA')
        width, height = 270, 330
        self.geometry(f'{width}x{height}+'
                      f'{(self.winfo_screenwidth() - width) // 2}+'
                      f'{(self.winfo_screenheight() - height) // 2}')
        self.resizable(False, False)

    def show_menus(self):
        """Функция отрисовки и инициализации менюшек"""
        settings_menu = Source.tk.Menu(tearoff=0)
        settings_menu.add_command(label="Общие настройки", command=lambda: SettingsWindow(self))
        settings_menu.add_command(label='Библиотека', command=lambda: LibraryWindow(self))
        information_menu = Source.tk.Menu(tearoff=0)
        information_menu.add_command(label='Информация по продуктам', command=lambda: InformationWindow(self))
        main_menu = Source.tk.Menu()
        main_menu.add_cascade(label="Настройки", menu=settings_menu)
        main_menu.add_cascade(label='Информация', menu=information_menu)
        self.config(menu=main_menu)
