import new_modules.Win.Source as Source
from new_modules.MailSamples import MailSamples


class MailSamplesWindow(Source.ChildWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Текстовые шаблоны')
        self.mail_samples = MailSamples()
        self.main()

    def main(self):
        self.show_listbox_widget()
        self.show_buttons_widgets()
        self.to_parent_center()
        self.resizable(False, False)
        self.focus()

    def show_listbox_widget(self):
        """Функция отрисовки виджета ListBox с прокрутокой содержимого"""
        self.__dict__['listbox_values'] = Source.tk.Variable(self, value=self.mail_samples.get_ms_list())
        frame = Source.tk.Frame(self)
        self.__dict__['listbox'] = Source.tk.Listbox(frame, width=50, listvariable=self.listbox_values)
        self.listbox.pack(side=Source.tk.LEFT)
        self.listbox.bind("<Return>", self.init_sample)
        scrollbar = Source.ttk.Scrollbar(master=frame, orient=Source.tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=Source.tk.RIGHT, fill=Source.tk.Y)
        self.listbox.config(yscroll=scrollbar.set)
        frame.pack()

    def show_buttons_widgets(self):
        """Функция отрисовки кнопок взаимодействия"""
        init_btn = Source.MyButton(self, text='Использовать', command=self.init_sample)
        init_btn.pack(side=Source.tk.LEFT, padx=2, pady=2)
        close_btn = Source.MyButton(self, text='Закрыть', command=self.destroy)
        close_btn.pack(side=Source.tk.RIGHT, padx=2, pady=2)

    def init_sample(self, event=None):
        """Копирование шаблона в буфер обмена. Если нет литералов - копируется сразу, если есть, то появляется
        окно-помошник для заполнения пропусков"""
        index = self.listbox.curselection()
        if not index:
            return
        self.mail_samples.create_sample(index[0])
        if len(self.mail_samples.SAMPLE) == 1:
            string = self.mail_samples.SAMPLE[0]
        else:
            AssistWindow(self)
            string = ''.join(self.mail_samples.SAMPLE)
        self.clipboard_clear()
        self.clipboard_append(string)
        Source.tkmb.showinfo(title='Текстовый шаблон', message='Текстовый шаблон скопирован в буфер обмена')
        self.focus()


class AssistWindow(Source.ChildWindow):
    """Вспомогательный класс, который вызывается когда в текстовом шаблоне присутствуют переменные значения"""
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.widget_lst = []
        self.mail_samples = MailSamples()
        self.main()
        self.bind("<Return>", self.create_string)
        self.focus()

    def main(self):
        self.overrideredirect(True)
        self.config(border=1, relief='solid')
        label = Source.ttk.Label(self, text='Заполните поля:')
        label.pack()
        self.show_entry_widget()
        enter_btn = Source.MyButton(self, text='Ввод', command=self.create_string, width=10)
        enter_btn.pack(padx=2, pady=2)
        self.to_parent_center()

    def show_entry_widget(self):
        """Функция отрисовки Entry виджетов для ввода информации в шаблон"""
        for variable in self.mail_samples.SAMPLE[1::2]:
            label = Source.ttk.Label(self, text=variable)
            label.pack(anchor=Source.tk.NW)
            entry = Source.ttk.Entry(self, width=30)
            entry.pack(padx=2)
            self.widget_lst.append(entry)

    def create_string(self, event=None):
        """Функция для сбора шаблона из введенных значений"""
        for i in range(1, len(self.mail_samples.SAMPLE), 2):
            self.mail_samples.SAMPLE[i] = self.widget_lst[i // 2].get()
        self.destroy()
