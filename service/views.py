import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from service.cron import send_email_tasks
from service.forms import MailingForm
from service.models import Mailing, Client, MailingMessage, Blog, MailingLog


@cache_page(60)
def home(request):
    """Домашняя страница с выводом списка всех созданных, но не проведенных рассылок"""
    posts = Blog.objects.all()  # получаем все статьи в блоге
    posts_for_context = []
    if len(posts) > 3:
        for i in range(3):
            number = random.randint(0, len(posts))
            posts_for_context.append(posts[number])
            print(posts[number])
    else:
        posts_for_context = posts
    # если у пользователя есть права
    if request.user.has_perm('service.can_disable_mailings'):
        mailing_list = Mailing.objects.filter(status=2 or 3)  # все активные или созданные рассылки
        mailing_all = Mailing.objects.all()  # все рассылки, созданные в сервисе

    else:
        mailing_list = Mailing.objects.filter(status=2 or 3,
                                              owner=request.user.pk)  # все активные или созданные рассылки пользователя
        mailing_all = Mailing.objects.filter(owner=request.user.pk)  # все рассылки пользователя

    count_clients = Client.objects.all()  # количество клиентов для рассылок
    context = {'object_list': mailing_list, 'title': 'Список активных рассылок',
               'count_active_mailings': len(mailing_list),
               'count_mailings': len(mailing_all),
               'posts': posts_for_context,
               'count_clients': len(count_clients)}  # создание контекста для передачи в render
    return render(request, 'service/home.html', context)


class MailingListView(ListView):
    """Класс-представление для вывода всех имеющихся рассылок"""
    model = Mailing
    template_name = 'service/mailings_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Список всех рассылок'
        return context

    def get_queryset(self):
        """фильтрация всех рассылок, созданных текущим пользователем"""

        # Если у пользователя есть права на отключение любой рассылки
        if self.request.user.has_perm('service.can_disable_mailings'):
            return super().get_queryset()

        # Иначе пользователю доступны только созданные им рассылки
        else:
            return Mailing.objects.filter(owner=self.request.user.pk)


class MailingCreateView(CreateView, LoginRequiredMixin):
    """Класс-представление для создания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('service:home')

    def form_valid(self, form):
        """Добавление в создаваемый продукт информации об авторизованном пользователе"""

        mailing = form.save()  # сохранение информации о созданной рассылке
        mailing.owner = self.request.user  # присваиваем атрибуту owner ссылку на текущего пользователя
        send_email_tasks()
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView, LoginRequiredMixin):
    """Класс-представление для редактирования рассылки"""

    model = Mailing
    fields = ('date_time', 'periodicity', 'client', 'status', 'message')
    success_url = reverse_lazy('service:home')


class MailingDeleteView(DeleteView, LoginRequiredMixin):
    """Класс-представление для удаления рассылки"""

    model = Mailing
    success_url = reverse_lazy('service:home')


class ClientCreateView(CreateView, LoginRequiredMixin):
    """Класс-представление для создания клиента"""

    model = Client
    success_url = reverse_lazy('service:create')
    fields = ('email', 'name', 'surname', 'patronymic', 'comment')


class MessageCreateView(CreateView, LoginRequiredMixin):
    """Класс-представление для создания сообщения"""

    model = MailingMessage
    fields = ('title', 'message')
    success_url = reverse_lazy('service:create')


def disable_mailing(pk):
    """функция для отключения рассылок"""

    mailing_for_disable = Mailing.objects.get(pk=pk)
    mailing_for_disable.status = 1
    mailing_for_disable.save()
    return redirect(reverse('service:mailings'))


class MailingLogList(ListView, LoginRequiredMixin):
    """Класс-представление для вывода лога проведенных рассылок"""
    model = MailingLog
    template_name = 'service/mailinglog_list.html'

    def get_queryset(self):
        """Если пользователь имеет права суперпользователя, ему возвращаются логи по всем проведенным рассылкам,
        иначе только по рассылкам, созданным текущим авторизованным пользователем"""

        return MailingLog.objects.filter(mailing__owner=self.request.user)


class MailingMessagesList(ListView, LoginRequiredMixin):
    """Класс-представление для вывода списка сообщений, созданных в сервисе"""
    model = MailingMessage

    def get_queryset(self):
        """Если пользователь обладает правами суперпользователя, ему возвращаются все сообщения, созданные в системе,
        иначе только сообщения, созданные текущим авторизованным пользователем"""

        if self.request.user.is_superuser:
            return super().get_queryset()

        return MailingMessage.objects.filter(owner=self.request.user)


class ClientListView(ListView, LoginRequiredMixin):
    model = Client

    def get_queryset(self):
        """Если пользователь имеет права суперпользователя, ему возвращаются все клиенты, созданные в системе,
        иначе только клиенты, созданные текущим авторизованным пользователем"""

        if self.request.user.is_superuser:
            return super().get_queryset()
        return Client.objects.filter(owner=self.request.user)
