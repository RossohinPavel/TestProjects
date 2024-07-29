from django.shortcuts import render
from .service import forecast


# Create your views here.
def index(request):
    """Отображение основной страницы"""
    data = {}
    if request.method == 'POST':
        res = forecast.get_forecast(request.POST['city'])
        if isinstance(res, str):
            data['error'] = res
        else:
            data['forecast'] = res
    return render(request, 'app/index.html', context=data)
