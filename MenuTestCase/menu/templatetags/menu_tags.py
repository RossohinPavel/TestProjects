from django import template
from menu.models import Menu
from django.db.models import Q



register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, title=None, menus=None):
	if menus is None:
		stmt = Q(title=title)
		paths = context.request.path.split('/')[1:-1]
		for path in paths:
			stmt = stmt | Q(title=path)
		menus = list(Menu.objects
			.filter(stmt)
			.select_related()
		)
		if len(menus) > 1 and menus[-1].parent.title != title:
			menus.pop(-1)
	else:
		menus.pop(0)

	dct = {
		'title': title,
		'context': context,
		'menus': menus
	}
	return dct
