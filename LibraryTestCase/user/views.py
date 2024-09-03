from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegisterUserForm, LoginUserForm, UpdateUserForm
from django.contrib.auth.decorators import login_required


# Create your views here.
class RegisterUserView(CreateView):
    """Вьюха для регистрации пользователя"""
    form_class = RegisterUserForm
    template_name = 'user/logreg.html'
    extra_context = {
        'title': "Регистрация",
        'button_label': 'Зарегистрироваться'
        }
    success_url = reverse_lazy('login')


class LoginUserView(LoginView):
    """Вьюха для авторизации пользователя"""
    form_class = LoginUserForm
    template_name = 'user/logreg.html'
    extra_context = {
        'title': "Авторизация",
        'button_label': 'Войти'
    }
    success_url = reverse_lazy('home')


@login_required
def update_user(request):
    """Вьюха для обновления информации о пользователе"""
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('home'))
    else:
        form = UpdateUserForm(instance=request.user)
    context = {
        'form': form,
        'title': 'Карточка ' + ('сотрудника' if request.user.is_staff else 'пользователя'),
        'button_label': 'Обновить'
    }
    return render(request, 'user/logreg.html', context=context)
