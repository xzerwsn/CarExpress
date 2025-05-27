from django import forms
from .models import Contact, Manufacturer, CarModel

class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы и placeholder'ы для всех полей
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })
        # Особые настройки для textarea
        self.fields['message'].widget.attrs.update({
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Введите ваше сообщение...'
        })

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'Ваше имя',
            'email': 'Email адрес',
            'message': 'Сообщение'
        }

class CarFilterForm(forms.Form):
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label='Производитель'
    )
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(),  # Начинаем с пустого queryset
        required=False,
        label='Модель'
    )
    min_price = forms.DecimalField(
        required=False,
        label='Минимальная цена',
        min_value=0,
        decimal_places=2
    )
    max_price = forms.DecimalField(
        required=False,
        label='Максимальная цена',
        min_value=0,
        decimal_places=2
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Если в данных формы уже есть выбранный производитель
        if 'manufacturer' in self.data:
            try:
                manufacturer_id = int(self.data.get('manufacturer'))
                self.fields['model'].queryset = CarModel.objects.filter(
                    manufacturer_id=manufacturer_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass