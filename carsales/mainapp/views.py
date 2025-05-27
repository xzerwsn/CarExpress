from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from mainapp.models import Car, Manufacturer, CarModel
from mainapp.forms import FeedbackForm, CarFilterForm

def index(request):
    form = FeedbackForm()
    message = None

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Здесь вы можете добавить код для обработки данных формы,
            # например, отправка письма или сохранение в базе данных.
            message = "Спасибо за ваше сообщение!"
            form = FeedbackForm()  # сбрасываем форму после успешного отправления
        else:
            message = "Ошибка при отправке. Пожалуйста, проверьте ваши данные."

    return render(request, 'index.html', {'form': form, 'message': message})

def get_models(request):
    manufacturer_id = request.GET.get('manufacturer')
    models = CarModel.objects.filter(manufacturer_id=manufacturer_id).order_by('name')
    data = {
        'models': [{'id': model.id, 'name': model.name} for model in models]
    }
    return JsonResponse(data)

class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True)
        form = CarFilterForm(self.request.GET)
        
        if form.is_valid():
            manufacturer = form.cleaned_data.get('manufacturer')
            model = form.cleaned_data.get('model')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            
            if manufacturer:
                queryset = queryset.filter(car_model__manufacturer=manufacturer)
            if model:
                queryset = queryset.filter(car_model=model)
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CarFilterForm(self.request.GET)
        return context

class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
