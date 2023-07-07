from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views import dashboard, create_booking, profile, add_field, owner_detail, main, field_detail


urlpatterns = [
    path('fields/', views.field_list, name='field_list'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', views.logoutUser, name='logout'),  # Изменен URL-путь для выхода из системы
    path('create-booking/', create_booking, name='create_booking'),
    path('add_field/', add_field, name='add_field'),
    path('profile/', profile, name='profile'),
    path('owner_detail/', owner_detail, name='owner_detail'),

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('field/<int:pk>/', views.field_detail, name='field_detail'),
    path('', main, name='main')

    ]
