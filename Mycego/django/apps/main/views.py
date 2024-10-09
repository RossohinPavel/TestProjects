from django.shortcuts import render, redirect
from .forms import UrlForm
from .service import get_file_data

# Create your views here.
def index(request):
	form = UrlForm(request.GET)
	# Для очистки формы от успешно введеной ссылки
	if request.GET.get('url') is None or form.is_valid():
		context = {'form': UrlForm()}
	else:
		context = {'form': form}

	if form.is_valid():
		link = form.cleaned_data['url']
		if link:
			context['data'] = get_file_data(link)
			context['data']['back_url'] = request.GET.get('back_url', None)
			context['data']['select'] = request.GET.get('select', '__all__')
	return render(request, 'index.html', context=context)
