from datetime import datetime, timedelta
from django.core.mail import send_mail
from config import settings
from service import models


def send_mailing(recipients) -> None:
    """Отправка рассылки клиентам из списка recipients"""
    print('отправка...')
    emails = recipients.client.values('email')  # список почтовых адресов для рассылки
    title = recipients.message.title  # тема письма
    text = recipients.message.message  # текст письма

    for email in emails:
        try:
            send_mail(title,  # Тема письма
                      text,
                      settings.EMAIL_HOST_USER,  # От кого письмо
                      recipient_list=[email['email']])  # попытка отправить письмо
            status = 'success'
            answer = 'Письмо отправлено успешно!'

        # Если при отправке письма возникает ошибка
        except Exception as err:
            status = 'error'
            answer = str(err)

        models.MailingLog.objects.create(status=status, answer=answer, mailing=recipients)  # создание записи в логе


def send_email_tasks():
    """Функция для управления рассылками"""
    print('Функция для управления рассылками')
    now = datetime.now()  # текущая дата
    mailings = models.Mailing.objects.filter(status__in=[2, 3])  # рассылки со статусом создана или запущена

    to_send = False  # флаг отправки

    for mailing in mailings:

        # если текущее время совпадает с временем рассылки
        if mailing.date_time.strftime('%H:%M') == now.strftime('%H:%M'):
            last_log = models.MailingLog.objects.filter(mailing=mailing.id).last()  # последняя попытка отправки

            # если рассылка еще не отправлялась
            if not last_log:
                to_send = True  # флаг отправки принимает значение True

            # Если рассылка уже отправлялась
            else:
                # вычисление разницы между текущей датой и последней попыткой отправки
                from_last = now.date() - last_log.date_time.date()

                # если периодичность отправки - раз в день и последняя попытка была один день назад
                if mailing.periodicity == 1 and from_last == timedelta(days=1):
                    print('day')
                    to_send = True  # флаг отправки принимает значение True

                # если периодичность отправки - раз в неделю и последняя попытка была семь дней назад
                elif mailing.periodicity == 2 and from_last == timedelta(days=7):
                    print('week')
                    to_send = True  # флаг отправки принимает значение True

                # если периодичность отправки - раз в месяц и последняя попытка была 30 дней назад
                elif mailing.periodicity == 3 and from_last == timedelta(days=30):
                    print('month')
                    to_send = True  # флаг отправки принимает значение True
        # если флаг отправки True - запуск рассылки
        if to_send:
            send_mailing(mailing)


