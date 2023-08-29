from django import forms

from service.models import Mailing


class MailingForm(forms.ModelForm):
    """Класс-представление для создания рассылки"""

    class Meta:
        model = Mailing

        fields = ('date_time', 'periodicity', 'client', 'message')

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
