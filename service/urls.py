from django.urls import path

from service.apps import ServiceConfig
from service.views import home, MailingCreateView, MailingUpdateView, MailingDeleteView, ClientCreateView, \
    MessageCreateView, MailingListView, disable_mailing, MailingLogList, MailingMessagesList, ClientListView

app_name = ServiceConfig.name

urlpatterns = [
    path('', home, name='home'),  # Домашняя страница
    path('create/', MailingCreateView.as_view(), name='create'),  # Страница создания рассылки
    path('update/<int:pk>', MailingUpdateView.as_view(), name='update'),  # Страница редактирования рассылки
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete'),  # Страница удаления рассылки
    path('clients/create', ClientCreateView.as_view(), name='create_client'),  # Страница создания клиента для рассылки
    path('message/create', MessageCreateView.as_view(), name='create_message'),  # Страница создания сообщения рассылки
    path('mailings/', MailingListView.as_view(), name='mailings'),  # Страница - список рассылок
    path('mailings/disable/<int:pk>', disable_mailing, name='disable'),  # Страница с отключением рассылки
    path('log/', MailingLogList.as_view(), name='log'),  # Страница с логами
    path('messages/', MailingMessagesList.as_view(), name='messages'),  # Страница - список сообщений
    path('clients/', ClientListView.as_view(), name='clients')  # страница - список клиентов
]