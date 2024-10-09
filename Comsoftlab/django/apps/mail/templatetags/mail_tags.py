"""Содержит тэги приложения mail"""
from django.template import Library


register = Library()


@register.inclusion_tag('mail_row.html')
def get_mail_row(mail = None):
    """Возвращает html-разметку для mail-записи"""
    return {
        'id': mail.id,
        'subject': mail.subject,
        'dispatch_date': str(mail.dispatch_date)[:10],
        'receive_date': str(mail.receive_date)[:10],
        'text': mail.text,
        'files': mail.files or '-'
    }
