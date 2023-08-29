from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    pass


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('service:home')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class UsersListView(ListView):
    model = User

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Список зарегистрированных пользователей сервиса'
        return context


def activate_new_user(request, pk):
    """Функция для активации нового пользователя"""
    user = get_user_model()  # получение модели пользователя
    user_for_activate = user.objects.get(id=pk)  # получение пользователя с нужным id
    user_for_activate.is_active = True  # смена флага у пользователя на True
    user_for_activate.save()  # сохранение
    return render(request, 'users/activate_user.html')


def block_user(request, pk):
    """Контроллер для управления активностью зарегистрированных в системе пользователей"""

    user_for_block = User.objects.get(id=pk)  # пользователь для блокировки

    # проверка статуса активности
    if user_for_block.is_active:
        user_for_block.is_active = False
    else:
        user_for_block.is_active = True

    user_for_block.save()

    return redirect(reverse('users:users_list'))  # перенаправление на страницу со списком пользователей