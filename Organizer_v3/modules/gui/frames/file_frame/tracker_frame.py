from ...source import *


class TrackerFrame(ttk.Frame):
    """Фрейм для отображения статуса и работы с трекером заказов."""

    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)

        HeaderLabel(self, text='Трекер заказов', anchor='n').pack(fill=ttkc.X)

        lbl1 = ttk.Label(self, text='Статус:', style='minipadding.TLabel')
        lbl1.pack(side=ttkc.LEFT)

        lbl2 = ttk.Label(self, style='minipadding.TLabel', text=APP.desc.ot_status._value)
        lbl2.pack(side=ttkc.LEFT, expand=1, anchor=ttkc.W)
        APP.desc.ot_status.add_call(lambda v: lbl2.configure(text=v))    #type: ignore

        control_btn = ttk.Button(
            self, 
            width=12,
            padding=2,
            text='Управление',
        )
        control_btn.configure(command=self.cmd_draw_popup_menu(control_btn))
        control_btn.pack(side=ttkc.LEFT)
    
    def cmd_change_log_check_depth(self) -> None:
        """Запрос на изменения настроек."""
        res = Querybox.get_integer(
            parent=self.master,
            title='Глубина проверки',
            prompt='Введите новое значение:',
            initialvalue=APP.stg.log_check_depth,
            minvalue=0,
        )
        if isinstance(res, int) and res > 0: 
            APP.stg.log_check_depth = res
        
    def cmd_draw_popup_menu(self, btn: ttk.Button):
        """Настраивает меню и возвращает ф-ю отрисовки"""
        match APP.OS_NAME:
            case 'nt': ix, iy = 116, 56
            case 'posix' | _: ix, iy = 90, 68

        menu = ttk.Menu(self, tearoff=0)

        var = ttk.IntVar(self, value=0)
        menu.add_checkbutton(
            label='Автоматический режим',
            offvalue=0,
            onvalue=1,
            command=lambda: setattr(APP.SETTINGS, 'autolog', var.get()),
            variable=var
        )
        APP.desc.autolog.add_call(var.set)

        menu.add_command(
            label='Глубина проверки', 
            command=self.cmd_change_log_check_depth
        )

        menu.add_command(
            label='Ручное обновление',
            command=lambda: APP.ORDER_TRACKER.manual_init()
        )
        
        return lambda: menu.tk_popup(btn.winfo_rootx() - ix, btn.winfo_rooty() - iy)
