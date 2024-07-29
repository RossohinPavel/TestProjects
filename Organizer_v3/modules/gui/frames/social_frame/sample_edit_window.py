from ...source import *


class SampleEditWindow(ChildWindow):
    """Окно редактирования/добавление текстового шаблона"""
    width = 380
    height = 450

    def __init__(self, sample_name: str | None = None) -> None:
        self._sample_name = sample_name
        self._tagw: ttk.Combobox
        self._namew: ttk.Entry
        self._textw: ttk.Text

        super().__init__()
        self._tagw.focus_set()

    def main(self, **kwargs) -> None:
        self.update_title()
        self.draw_tag_and_name_widgets()
        self.draw_text_field()
        self.draw_buttons()
        self.insert_values(APP.ms.get(self._sample_name) if self._sample_name else self.get_default_text())
    
    def update_title(self) -> None:
        """Обновление заголовка окна."""
        pre, title = 'Редактирование: ', self._sample_name
        if title is None:
            pre, title = 'Добавление шаблона', ''
        self.title(f'{pre}{title}')

    def draw_tag_and_name_widgets(self) -> None:
        """Отрисовка видежетов редактирования тэга и имени шаблона."""
        frame = ttk.Frame(self)
        frame.pack(fill=ttkc.X, pady=5, padx=5)
        frame.columnconfigure(1, weight=1)

        tags = set(x[0] for x in APP.ms.get_headers())

        # Строчка тэга
        ttk.Label(frame, text='Тэг:').grid(row=0, column=0, padx=(0, 5), pady=(0, 5))
        self._tagw = ttk.Combobox(
            frame, 
            cursor='xterm', 
            values=sorted(tags)
        )
        self._tagw.grid(row=0, column=1, sticky=ttkc.EW, pady=(0, 5))

        # Строчка имени
        ttk.Label(frame, text='Имя:').grid(row=1, column=0, padx=(0, 5))
        self._namew = ttk.Entry(frame)
        self._namew.grid(row=1, column=1, sticky=ttkc.EW)

    def draw_text_field(self) -> None:
        """Отриосовка текстового поля редактирования шаблона."""
        frame = ttk.Frame(master=self)
        frame.pack(expand=1, fill=ttkc.BOTH, padx=5)

        # Текстовое поле
        self._textw = ttk.Text(frame, width=2, height=2, wrap='word')
        self._textw.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1)

        # Бинд на выделение слова
        self._textw.bind('<Control-space>', self.highlight_event)

        # СкроллБар
        scroll = ttk.Scrollbar(frame, command=self._textw.yview, style='round')
        self._textw.config(yscrollcommand=scroll.set)
        scroll.pack(side=ttkc.RIGHT, fill=ttkc.Y)
    
    def draw_buttons(self) -> None:
        """Отрисовка кнопок Сохранения и Отмены"""
        save = ttk.Button(
            master=self, 
            text='Сохранить', 
            width=18, 
            style='success',
            padding=2,
            command=self.save
            )
        save.pack(pady=5, padx=5, side=ttkc.LEFT)

        cancel = ttk.Button(
            master=self, 
            text='Отмена', 
            width=18, 
            style='danger',
            padding=2,
            command=self.destroy
        )
        cancel.pack(pady=5, padx=5, side=ttkc.RIGHT)

    def insert_values(self, sample_tpl: tuple[str, str, str]) -> None:
        """Размещает полученную информацию по виджетам"""
        self._tagw.insert('0', sample_tpl[0])
        self._namew.insert('0', sample_tpl[1])
        self._textw.insert('1.0',sample_tpl[2])

    def get_default_text(self) -> tuple[str, str, str]:
        """Получение информации по-умолчанию"""
        tag = 'Общие'
        name = 'Демонстрационный шаблон'
        text = (
            '############# Текстовые шаблоны #############\n\n',
            'Текстовые шаблоны (далее ТШ) служат для ускорения передачи информации. Но с большой силой ',
            'приходит и большая ответственность. Следует внимательно относиться к составлению, отправке и',
            ' удалению ТШ.\n\nДля добавления нового шаблона - вместо этой инструкции введите нужный текст. ',
            'Проверьте себя на грамматику, пунктуацию и, прежде всего, на простоту и полноту передаваемых смыслов.',
            '\n\nТШ поддерживают переменные элементы. При инициализации ТШ программа даст подсказку, что ',
            'подставить вместо переменного элемента. Если информация не была внесена в соответствующее ',
            'поле, то ничего подставлено не будет, а переменный элемент будет удален.\n\nДля добавления ',
            'переменного элемента выделите слово литералом ?% по образцу, указанному в примере. ',
            'Использовать такую комбинацию символов в других целях нельзя. ',
            'Комбинация клавиш <Control-space> вставляет ?%?% в позицию курсора.\n\n\n',
            '################## Пример ##################\n\n?%Имя?%, здравствуйте.\nВас беспокоит ',
            'ФотокнигиОптом, Киров.\nПо поводу заказа ?%Номер заказа?%.'
            )
        return tag, name, ''.join(text)

    def highlight_event(self, event: tkinter.Event) -> None:
        """Событие для выделения слово литералами в тексте шаблона"""
        self._tagw.insert('insert', '?%?%')

    def save(self) -> None:
        """Сохранение шаблона в библиотеку"""
        old_name = self._sample_name
        tag = self._tagw.get()
        name = self._namew.get()
        text = self._textw.get("1.0", "end")[:-1]
        if not name:
            tkmb.showwarning(parent=self, title='Предупреждение', message='Отсутствует имя шаблона')
            return
        try:
        # В зависимости от наличия тэга (существования шаблона) обновляем его или создаем новый
            if old_name:   
                APP.ms.update(old_name, tag, name, text)
            else:
                APP.ms.create(tag, name, text)
            self.destroy()
            tkmb.showinfo(
                parent=self.master, 
                title='Сохранение шаблона', 
                message=f'Шаблон <{name}> сохранен'
            )
        except Exception as E:
            tkmb.showerror(
                parent=self.master,
                title='Ошибка',
                message=f'Скорее всего, шаблон не уникален.\n{E}'
            )