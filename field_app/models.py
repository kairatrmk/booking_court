import datetime, os
from decimal import Decimal
from django.db import models
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# class OwnerProfile(models.Model):
#     # owner = models.OneToOneField(Owner, on_delete=models.CASCADE, verbose_name='Владелец')
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Другие поля профиля владельца поля

#     def __str__(self):
#         return self.user.username
    

class Owner(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя владельца')
    address = models.CharField(max_length=200, verbose_name='Адрес', null=True)
    contact = models.CharField(max_length=100, verbose_name='Контактные данные', default='+996')
    # user_profile = models.OneToOneField(OwnerProfile, on_delete=models.CASCADE, verbose_name='Профиль пользователя')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', default=1)

    # Другие поля для владельца

    def __str__(self):
        return self.name
    
    class Meta():
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'


class Field(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='Владелец')
    name = models.CharField(max_length=100, verbose_name='Поле')
    has_shower = models.BooleanField(default=False, verbose_name='Наличие душа')
    photo = models.ImageField(upload_to='fields/', blank=True, null=True)
    has_roof = models.BooleanField(default=False, verbose_name='Крытое/Некрытое')
    has_parking = models.BooleanField(default=False, verbose_name='Наличие парковки')
    has_locker_room = models.BooleanField(default=False, verbose_name='Наличие раздевалки')
    surface_type = models.CharField(max_length=100, verbose_name='Тип покрытия', choices=(
        ('газон', 'Газон'),
        ('паркет', 'Паркет'),
    ), default='Газон')
    size_of_field = models.CharField(max_length=100, verbose_name='Размер поля', default='Длина:  Ширина: ')

    
    # Другие поля для поля

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'


class Booking(models.Model):
    TIME_CHOICES = [(f"{hour:02d}:{minute:02d}", f"{hour:02d}:{minute:02d}") for hour in range(0, 24) for minute in (0, 30)]

    # owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, verbose_name='Владелец')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, verbose_name='Владелец', related_name='booking')

    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name='Поле')
    selected_date = models.DateField(verbose_name='Выбранная дата')
    selected_time_start = models.CharField(max_length=5, choices=TIME_CHOICES, verbose_name='Начальное время')
    selected_time_end = models.CharField(max_length=5, choices=TIME_CHOICES, verbose_name='Конечное время')
    played_hours = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сыгранное время', null=True, blank=True)
    price_hour = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за час')
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговый счет', blank=True, null=True)


    def clean(self):
        # Проверка, что конечное время больше начального времени
        if self.selected_time_start and self.selected_time_end:
            selected_start_hour, selected_start_minute = map(int, self.selected_time_start.split(':'))
            selected_start_time = datetime.time(selected_start_hour, selected_start_minute)

            selected_end_hour, selected_end_minute = map(int, self.selected_time_end.split(':'))
            selected_end_time = datetime.time(selected_end_hour, selected_end_minute)

            if selected_end_time < selected_start_time:
                # Разница переходит на следующий день
                diff = datetime.timedelta(hours=24) - datetime.datetime.combine(datetime.date.today(), selected_start_time) + datetime.datetime.combine(datetime.date.today(), selected_end_time)
            else:
                diff = datetime.datetime.combine(datetime.date.today(), selected_end_time) - datetime.datetime.combine(datetime.date.today(), selected_start_time)

            played_hours = diff.seconds / 3600  # Преобразование разницы в часы
            if played_hours < 0:
                played_hours += 24  # Добавляем 24 часа, если разница переходит на следующий день

            if played_hours % 0.5 != 0:
                raise ValidationError("Сыгранное время должно быть кратно 0.5 часа")

            self.played_hours = played_hours

        else:
            raise ValidationError("Выберите начальное и конечное время игры")

    
    def save(self, *args, **kwargs):
        # Расчет значения total_bill
        if self.selected_time_start and self.selected_time_end and self.price_hour:
            selected_hour_start, selected_minute_start = map(int, self.selected_time_start.split(':'))
            selected_hour_end, selected_minute_end = map(int, self.selected_time_end.split(':'))
            start_time = datetime.time(selected_hour_start, selected_minute_start)
            end_time = datetime.time(selected_hour_end, selected_minute_end)
            played_hours = Decimal((end_time.hour - start_time.hour) + (end_time.minute - start_time.minute) / 60)
            self.total_bill = played_hours * self.price_hour

        super().save(*args, **kwargs)


    class Meta():
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class Photo(models.Model):
    field = models.ForeignKey(Field, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')



from django.db import models
from .models import Field


class TimeSlot(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name='Поле', related_name='time_slots')
    start_time = models.DateTimeField(verbose_name='Начало')
    end_time = models.DateTimeField(verbose_name='Окончание')
    is_booked = models.BooleanField(default=False, verbose_name='Занято')

    def clean(self):
        if self.field and self.start_time and self.end_time:
            # Проверка наличия других занятых слотов для данного поля и временного диапазона
            is_booked = TimeSlot.objects.filter(
                field=self.field,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
                is_booked=True
            ).exists()
            self.is_booked = is_booked

        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.field} - {self.start_time} to {self.end_time}"
