from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.mail import send_mail

from config import settings
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        template_name = 'users/register.html'

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        """смена у пользователя флага на неактивный и отправка на почту пользователя
        письма с ссылкой на активацию"""

        user = super().save()  # сохраение в переменной пользователя
        send_mail(subject='Активация',
                  message=f'Для активации профиля пройдите по ссылке - http://127.0.0.1:8000/users/activate/{user.id}/',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[user.email])  # отправка письма на почту
        user.is_active = False  # смена флага на неактивный
        user.save()  # сохранение
        return user


class UserProfileForm(UserChangeForm):

        class Meta:
            model = User
            fields = ('email', 'phone', 'avatar', 'country')

        def __init__(self, *args, **kwargs):
            """Стилизация формы"""
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

            self.fields['password'].widget = forms.HiddenInput()


class UserProfileForm:
    pass