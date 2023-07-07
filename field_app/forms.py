from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Field, Owner


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']    
    
class OwnerLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['field', 'selected_date', 'selected_time_start', 'selected_time_end', 'price_hour']


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'has_shower', 'photo', 'has_roof', 'has_parking', 'has_locker_room', 'surface_type', 'size_of_field']

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'address', 'contact']