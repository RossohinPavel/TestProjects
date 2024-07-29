from django import template



register = template.Library()


@register.inclusion_tag('app/table_row.html')
def list_to_table_row(name: str, data: list, suff=''):
	"""Тэг шаблона для превращения в строку таблицы"""
	return {'name': name, 'data': data, 'suff': suff}
