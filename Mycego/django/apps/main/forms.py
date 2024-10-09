from django import forms


class UrlForm(forms.Form):
	"""Форма для отрисовки и валидации url"""
	url = forms.URLField(
		label='', 
		widget=forms.TextInput(
			attrs={'class': 'form-control form-control-lg'}
		),
		required=False
	)
