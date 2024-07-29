from ...source import *
from ...source import images
from .init_sample_window import InitSampleWindow
from .sample_edit_window import SampleEditWindow


class SampleLine(ttk.Frame):
    """Фрейм-Интерфейс для работы с текстовыми шаблонами."""

    def __init__(self, master: Any, sample_name: str):
        super().__init__(master)
        self._sample_name = sample_name

        btn1 = ttk.Button(
            self,
            style='ljf.TButton',
            padding=(5, 2, 2, 2),
            text=sample_name,
            command=self.init_sample
        )
        btn1.pack(side=ttkc.LEFT, expand=1, fill=ttkc.X)

        btn2 = ttk.Button(
            self,
            padding=1,
            image=images.GEAR
        )
        btn2.configure(command=self.context_command(btn2))
        btn2.pack(side=ttkc.LEFT, fill=ttkc.Y)

    def context_command(self, btn: ttk.Button):
        """Замыкание для предостовления команды для отрисовки меню на кнопке шестеренки."""
        menu = ttk.Menu(self, tearoff=0)
        menu.add_command(label='Использовать', command=self.init_sample)
        menu.add_command(label='Изменить', command=self.edit_sample)
        menu.add_command(label='Удалить', command=self.del_sample)
        menu.add_command(label='Содержание', command=self.see_sample)

        def inner():
            x, y = btn.winfo_rootx(), btn.winfo_rooty()
            indent = 100 if APP.OS_NAME == 'nt' else 80
            menu.tk_popup(x - indent, y + btn.winfo_height())

        return inner

    def del_sample(self) -> None:
        """Удаление текстового шаблона."""
        APP.ms.delete(self._sample_name)
        self.master.master.update_frame()

    def edit_sample(self) -> None:
        """Редактирование текстового шаблона."""
        self.wait_window(SampleEditWindow(self._sample_name))
        self.master.master.update_frame()

    def init_sample(self) -> None:
        """Инициализация текстового шаблона"""
        tag, sample_name, text = APP.ms.get(self._sample_name)
        sample_title = f'{tag} - {sample_name}'
        text = text.split('?%')

        if len(text) > 1:
            self.wait_window(InitSampleWindow(sample_title, text))

        message = ''.join(text)
        if message:
            self.clipboard_clear()
            self.clipboard_append(message)
            tkmb.showinfo(title=sample_title, message='Шаблон скопирован в буфер обмена.')

    def see_sample(self) -> None:
        """Просмотр содержимого шаблона"""
        _, name, data = APP.ms.get(self._sample_name)
        tkmb.showinfo(parent=APP.mw, title=name, message=''.join(data))


class MailSamplesFrame(ScrolledFrame):
    """Фрейм для работы с текстовыми шаблонами"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, bootstyle='round', padding=5)
        self.update_frame()

    def update_frame(self) -> None:
        """Наделение листобокса именами текстовых шаблонов"""
        for i in self.winfo_children():
            i.destroy()
        
        # Отрисовка виджетов текстовых шаблонов
        current_tag = frame = None
        for tag, name in sorted(APP.ms.get_headers()):
            if current_tag != tag:
                current_tag = tag
                frame = ttk.LabelFrame(self, text=tag)
                frame.pack(fill='x', padx=(0, 12), pady=(0, 5))

            sl = SampleLine(frame, name)
            sl.pack(fill=ttkc.X, padx=5, pady=(0, 5))
            # sb = SampleButton(frame, self, name)
            # sb.pack(fill=ttkc.X, padx=5, pady=(0, 5))
        
        btn = ttk.Button(
            master=self, 
            width=16,
            padding=2,
            text='Добавить',
            command=self.add_sample, 
            style='success'
        )
        btn.pack(pady=(0, 5))
    
    def add_sample(self) -> None:
        """Добавление семпла в общий список"""
        self.wait_window(SampleEditWindow())
        self.update_frame()
