from ._handler import HandlerWindow
from ...file_handlers import PageDecoder


class PageDecoderWindow(HandlerWindow):
    win_title = 'Раскодировка Альбомов, Журналов и FlexBind'
    handler_description = 'Раскодировка Альбомов, Журналов и FlexBind\nсогласно особенности продукта. '\
                          'В каталоге тиража\nбудет создана папка Pages в которой будут\nсохранены поэкземплярно '\
                          'раскодированные тиражи.\nРаскодированные обложки у журналов будут сохранены\nв отдельную '\
                          'папку.\nПри выборе опции \'Бэкпринт и переименование экземпляров\'\nна раскодированные '\
                          'странички в альбомах и FlexBind будет\nнанесена информация о номере заказа, имени '\
                          'тиража и номере\nэкземпляра. К имени папки экземпляра будет добавлена\nинформация о '\
                          'количестве разворотов в нем.'
    handler_option_text = 'Бэкпринт и переименование экземпляров'
    file_handler = PageDecoder()

    def handler_predicate(self, product_obj) -> object | None:
        return product_obj if product_obj.category in ('Album', 'Journal') else None
