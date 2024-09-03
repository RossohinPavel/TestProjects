from django.template import Library


register = Library()


@register.simple_tag()
def get_book_btn(user, book):
    btn_title = "Читать"
    enabled = True
    if book.reader is not None:
        if book.reader == user:
            btn_title = "Вернуть"
        else:
            btn_title = "Занято"
            enabled = False
    return {"title": btn_title, "enabled": enabled, "book_id": book.pk}
