
from django.urls import path
from .views import CarListView, CarDetailView, get_models
from . import views

app_name = 'mainapp'  # Важно использовать правильное имя приложения

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', CarListView.as_view(), name='car_list'),
    path('<slug:slug>/', CarDetailView.as_view(), name='car_detail'),
    path('get-models/', get_models, name='get_models'),
]