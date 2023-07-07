from django.contrib import admin

from django.contrib import admin
from .models import Owner, Field, Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ('owner', 'field', 'selected_date', 'selected_time_start', 'selected_time_end', 'played_hours', 'price_hour', 'total_bill') 


class FieldAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'has_shower', 'has_parking', 'has_locker_room', 'surface_type', 'has_roof', 'photo', 'size_of_field')


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact') 


admin.site.register(Field, FieldAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Booking, BookingAdmin)
