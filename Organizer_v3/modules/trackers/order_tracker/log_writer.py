from ...data_base import Log
from .proxy_info import OrderInfoProxy
from .proxy_edition import EditionProxy
from .proxy_photo import PhotoProxy


class LogWriter(Log):
    """Класс предостовляющий доступ к записи лога заказов"""
    __slots__ = ()

    @Log.safe_connect
    def update_records(self, proxies: set[EditionProxy | PhotoProxy]) -> None:
        """Сборная ф-я для обновления библиотеки"""
        for proxy in sorted(proxies, key=lambda x: (x._order_proxy.name, x.name)):
            # Записываем информацию по заказу в лог, если к нам пришел непустой тираж
            if proxy._updated and proxy._order_proxy._updated:
                proxy._order_proxy._updated = False
                self.__update_table(proxy._order_proxy)
            
            # Пропускаем не обновившиеся прокси объекты
            if not proxy._updated: continue

            # Обновляем лог
            if isinstance(proxy, PhotoProxy):
                self.__update_photos(proxy)
            else:
                self.__update_table(proxy)
        self.connect.commit()

    def __update_table(self, proxy: OrderInfoProxy | EditionProxy) -> None:
        """Обновление данных в основной таблице информации о заказе"""
        self.cursor.execute(proxy.check_request)
        if self.cursor.fetchone()[0]:
            self.cursor.execute(*proxy.update_request)
        else:
            self.cursor.execute(*proxy.insert_request)
    
    def __update_photos(self, proxy: PhotoProxy) -> None:
        """Для записи фотопечати пришлось использовать отдельный метод"""
        for name in proxy.__dict__:
            self.cursor.execute(proxy.check_request(name))
            if self.cursor.fetchone()[0]:
                self.cursor.execute(*proxy.update_request(name))
            else:
                self.cursor.execute(*proxy.insert_request(name))

    @Log.safe_connect
    def get_newest_order_name(self) -> str:
        """Получение последнего сканированного номера заказа"""
        self.cursor.execute('SELECT MAX(name) FROM Orders')
        return self.cursor.fetchone()[0]
