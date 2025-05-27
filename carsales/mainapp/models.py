from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Контактное сообщение'
        verbose_name_plural = 'Контактные сообщения'

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=50)
    founded_year = models.PositiveIntegerField()
    logo = models.ImageField(upload_to='manufacturers/logos/', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    production_start = models.PositiveIntegerField()
    production_end = models.PositiveIntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.manufacturer.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"

class Car(models.Model):
    BODY_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('wagon', 'Wagon'),
        ('pickup', 'Pickup'),
    ]

    TRANSMISSION_TYPES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('cvt', 'CVT'),
    ]

    FUEL_TYPES = [
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]

    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    mileage = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    engine_size = models.DecimalField(max_digits=3, decimal_places=1)
    horsepower = models.PositiveIntegerField()
    body_type = models.CharField(max_length=20, choices=BODY_TYPES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_TYPES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.car_model.manufacturer.name}-{self.car_model.name}-{self.year}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.car_model} {self.year}"

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/images/')
    is_main = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"