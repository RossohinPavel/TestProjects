from django.shortcuts import render


# Create your views here.
def index(request, **kwargs):
	return render(request, 'menu/index.html', context=kwargs)
