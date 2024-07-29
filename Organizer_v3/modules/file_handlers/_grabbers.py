from ._iterators import *


class EditionGrabber(dict):
    """Предостовляет различные функции для выборки изображений из тиража"""
    __slots__ = ()

    def __init__(self, path: str, *mode: it_mode) -> None:
        # Формируем словарь
        for name, imgs in edition_iterator(path, *mode):
            self[name] = tuple(imgs)

    def covers_from_ex(self) -> Iterator[tuple[str, str, int]]:
        """
            Предоставляет генератор для итерации по обложкам из папок экземпляров.
            Возвращает имя экземпляра, имя обложки и количетсво разворотов в экземпляре.
        """
        for ex, images in self.items():
            if fullmatch(EXEMPLAR, ex):
                for cover in reversed(images):
                    if cover.startswith('cover'):
                        yield ex, cover, len(images) - 1
                        break

    def cover_from_constant(self) -> Iterator[tuple[str, str, int]]:
        """
            Предоставляет генератор для итерации по постоянным обложкам.
            Возвращает Constant, имя обложки и наибольшее количество разворотов в экземпляре.
        """
        count = 0
        for ex, images in self.items():
            if fullmatch(EXEMPLAR, ex):
                len_ex = len(images) - 1
                if len_ex > count:
                    count = len_ex
            if ex == 'Constant':
                for cover in reversed(images):
                    if cover.startswith('cover'):
                        yield ex, cover, count
                        break

    def pages_from_ex(self, constant=False, cover_included=False):
        """
            Предрставляет генератор для итерации по разворотам экземпляра.
            Возвращает имя экземпляра и генератор для итерации по именам разворотов.
            Если constant=True, то итерация обрывается после выдачи 1 результата, так как развороты постоянные
        """
        for ex, images in self.items():
            if fullmatch(r'\d{3}(-\d+_pcs)?', ex):
                yield ex, (x for x in images if not x.startswith('cover') or cover_included)
                if constant:
                    break

    def images_from_constant_iter(self, cover_included=False):
        """Ф-я для получения изображений из папки Constant"""
        if 'Constant' in self:
            yield from (x for x in self['Constant'] if not x.startswith('cover') or cover_included)
