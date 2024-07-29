from ...source import *


class OrdersStatWindow(ChildWindow):
    """Окно Статистики по заказам."""
    width, height = 550, 350
    win_title = 'Статистика'

    def main(self, **kwargs) -> None:
        for i in range(7):
            frame = self.draw_day_frame(i)
            frame.grid(
                row=0 if i < 4 else 1,
                column=i if i < 4 else i-4,
                pady=(5, 0),
                padx=(5, 0)
            )
    
    def draw_day_frame(self, num: int) -> ttk.LabelFrame:
        t = ttk.LabelFrame(self, text=f'2024-02-23 {num}')

        lbl1 = ttk.Label(t, text='Заказов: 26')
        lbl1.pack(anchor=ttkc.NW)

        lbl2 = ttk.Label(t, text='Обложек: 120')
        lbl2.pack(anchor=ttkc.NW)

        lbl3 = ttk.Label(t, text='Разворотов: 430')
        lbl3.pack(anchor=ttkc.NW)

        lbl4 = ttk.Label(t, text='Фотопечать: 1200')
        lbl4.pack(anchor=ttkc.NW)

        lbl5 = ttk.Label(t, text='Другое: 56')
        lbl5.pack(anchor=ttkc.NW)

        ttk.Frame(t, width=120).pack()

        ttk.Separator(t).pack(fill=ttkc.X)

        lbl7 = ttk.Label(t, text='Сложность: 104')
        lbl7.pack(anchor=ttkc.NW)

        return t