from django.contrib import admin
from .models import Contact, Manufacturer, CarModel, Car, CarImage

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

class CarAdmin(admin.ModelAdmin):
    list_display = ('car_model', 'year', 'price', 'is_available')
    list_filter = ('is_available', 'car_model__manufacturer', 'year', 'fuel_type')
    search_fields = ('car_model__name', 'car_model__manufacturer__name', 'description')
    inlines = [CarImageInline]

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'production_start', 'production_end')
    list_filter = ('manufacturer',)
    search_fields = ('name', 'manufacturer__name')

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')
    search_fields = ('name', 'country')

admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)