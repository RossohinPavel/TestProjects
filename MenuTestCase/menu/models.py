from django.db import models



class Menu(models.Model):
	title = models.CharField(max_length=100)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child')

	def __str__(self) -> str:
		return self.title



class MenuItem(models.Model):
	"""Модель меню и для всех вложенных меню"""
	title = models.CharField(max_length=100)
	url = models.CharField(max_length=100)
	menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')

	def __str__(self):
		return self.title
	
	def get_url(self):
		suf = '/'
		if self.menu.parent is not None:
			suf += self.menu.title + '/'
		return suf + self.url
