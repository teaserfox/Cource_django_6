from django.contrib import admin

from service.models import Client, MailingMessage, Mailing, Blog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Регистрация модели Client в админ-панели"""
    list_display = ['email', 'name', 'surname', 'patronymic', 'comment']


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    """Регистрация модели MailingMessage в админ-панели"""
    list_display = ['title', 'message']


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Регистрация модели Mailing в админ-панели"""
    list_display = ['date_time', 'periodicity', 'message']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Регистрация модели Blog"""
    list_display = ['title', 'description', 'image']
