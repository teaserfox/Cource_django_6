from django.db import models

from config import settings


# варианты периодичности рассылки (раз в день, в неделю, в месяц)
MAILING_PERIODICITY = [(1, 'раз в день'), (2, 'раз в неделю'), (3, 'раз в месяц')]

MAILING_STATUS = [(1, 'завершена'), (2, 'создана'), (3, 'запущена')]  # варианты статуса рассылки
NULLABLE = {'null': True, 'blank': True}  # для необязательного поля


class MailingMessage(models.Model):
    """Модель сообщение для рассылки"""

    title = models.CharField(max_length=100, verbose_name='Тема сообщения')  # Тема сообщения
    message = models.TextField(verbose_name='Тело сообщения')  # Тело сообщения
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.title


class Client(models.Model):
    """Модель клиента сервиса рассылок (того кому будем отправлять)"""

    email = models.CharField(max_length=100, verbose_name='Email')  # контактный email
    name = models.CharField(max_length=100, verbose_name='Имя')  # имя
    surname = models.CharField(max_length=100, verbose_name='Фамилия')  # фамилия
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')  # отчество
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)  # комментарий
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)  # Владелец (ссылка)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    """Модель настройки для рассылки"""

    date_time = models.DateTimeField(verbose_name='Время рассылки')  # время рассылки
    periodicity = models.PositiveSmallIntegerField(choices=MAILING_PERIODICITY, default=1)  # Периодичность
    status = models.PositiveSmallIntegerField(choices=MAILING_STATUS, default=2)  # статус рассылки
    client = models.ManyToManyField(Client)  # клиент рассылки
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE)  # сообщение для рассылки
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)  # Владелец (ссылка)

    def __str__(self):
        return f'Рассылка на {self.date_time} с периодичностью {self.periodicity}. Статус {self.status}'


    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [('can_view_mailings', 'can_view_mailings'),
                       ('can_disable_mailings', 'can_disable_mailings'),
                       ]


class MailingLog(models.Model):
    """Модель лог рассылки"""

    date_time = models.DateTimeField(auto_now_add=True)  # дата и время последней попытки (формируется автоматически)
    status = models.CharField(max_length=100, verbose_name='Статус попытки')  # статус попытки
    answer = models.CharField(max_length=100, verbose_name='Ответ сервера', **NULLABLE)  # ответ почтового сервера
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)  # рассылка

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'


class Blog(models.Model):
    """Модель блога"""

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='image/', verbose_name='Изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
