from django import template


register = template.Library()


@register.inclusion_tag('menu_item.html', takes_context=True)
def get_filter_menu_item(context, name='__all__', select='__all__'):
	"""Тег для рендера меню итемов"""
	style = "dropdown-item"
	if name == select:
		style += " active"
	params = (f'{key}={value}' for key, value in context['request'].GET.items() if key != 'select')
	return {
		"name": name, 
		'class': style, 
		'link': context['request'].path + "?" + "&".join(params) + f"&select={name}"
	}
