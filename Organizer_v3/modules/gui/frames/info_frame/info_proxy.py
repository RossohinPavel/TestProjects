from modules import app_manager as APP
from modules.utilits.order_proxy import OrderProxy
from typing import Iterator


class OrderInfoProxy(OrderProxy):
    """Прокси объект для генерации стикеров в заказе"""

    __slots__ = ()

    @staticmethod
    def get_edition_info(edition: APP.LOG.Edition) -> Iterator[str]:
        """Возвращает информацию о тираже в виде строки"""
        yield edition.name

        # Продукт и его определение
        product = edition.product
        yield f'Определился: {product.name if product else None}'

        # Количество обложек и их тип
        yield f'Обложек: {edition.covers}'
        if product and product.cover_type:
            yield f'Тип обложки: {product.cover_type}'
        
        # Количество разворотов и тип сборки блока
        if edition.pages is not None:
            yield f'Разворотов: {edition.pages}'
        if product and product.page_option:
            yield f'Тип сборки: {product.page_option}'
        
        # Комплексный счетчик
        yield f'Комплексно: {edition.ccount}'

        # Совмещение
        if edition.comp:
            yield f'Совмещение: {edition.comp}'
        
        # Старый стикер
        yield 'Стикер: ' + ' '.join(OrderInfoProxy.create_sticker(edition))

    @staticmethod
    def create_sticker(edition: APP.LOG.Edition) -> Iterator[str]:
        """Вспомагательная генераторная ф-я для формирования информации о тираже"""
        product = edition.product
        if edition.product is None:
            yield 'None'
            return

        # 1) Получаем и передаем короткое имя
        short_name = product.short_name
        yield short_name

        # 2) Если имя начинается на +, то это субпродукт. Для него достаточно вернуть количество
        if short_name.startswith('+'):
            yield f'{edition.covers}шт'
            return

        # 3) Передаем формат для книг. Для продуктов типа Дуо это не нужно
        if short_name not in ("Дуо", "Дуо гор", "Трио"):
            yield product.format

        # 4) Передаем колличественное представление. Для книг - комплексный счетчик, остальное - шутчно.
        if short_name in ("Дуо", "Дуо гор", "Трио"):
            yield f'{(edition.covers)}шт'
        else:
            yield edition.ccount

        # 4) Для книг возвращаем опции сборки
        if product.page_option: 
            yield product.page_option

        # 5) Для продуктов с лraise StopIterationаминацией возвращаем ламинацию
        if product.cover_lam: 
            yield product.cover_lam

        # 6) Если у тиража определилось совмещение (книг больше, чем 1), то возвращаем его.
        if edition.comp: 
            yield f'-- {edition.comp}'

        # 7) Для типа обложки Кожаный корешок возвращаем дополнительную строку
        if product.cover_type == 'Кожаный корешок':
            yield 'кож кор'
