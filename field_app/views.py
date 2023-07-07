from django.forms import ValidationError
from django.shortcuts import render, redirect
from .models import Field, Booking, Owner
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, BookingForm, FieldForm, OwnerForm
from django.contrib import messages
from field_app.models import Field, Booking, Owner
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from .models import Field, TimeSlot



def field_detail(request, field_id):
    field = get_object_or_404(Field, id=field_id)
    time_slots = TimeSlot.objects.filter(field=field)

    return render(request, 'field_app/field_detail.html', {'field': field, 'time_slots': time_slots})



def field_list(request):
    fields = Field.objects.all()
    bookings = Booking.objects.all()
    booked_dates = [booking for booking in bookings]
    available_fields = [field for field in fields if field not in booked_dates]
    return render(request, 'fut_pole/field_list.html', {'fields': fields})

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid(): 
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')
   

        context = {'form':form}
        return render(request, 'field_app/registration.html', context)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('main')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('main')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'field_app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')



@login_required
def dashboard(request):
    return render(request, 'field_app/dashboard.html')

def logoutUser(request):
    logout(request)
    return redirect('main')

def create_booking(request):
    owner = request.user.owner

    fields = Field.objects.filter(owner=owner)
    
    time_choices = Booking.TIME_CHOICES

    context = {
        'fields': fields,
        'time_choices': time_choices,
    }
        
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            owner = Owner.objects.get(user=request.user)  # Получаем владельца по текущему пользователю
            booking.owner = owner
            
            selected_date = booking.selected_date
            selected_time_start = booking.selected_time_start
            selected_time_end = booking.selected_time_end
            
            # Проверяем, существует ли уже заказ для данного владельца на выбранную дату и временной диапазон
            existing_booking = Booking.objects.filter(
                owner=owner,
                selected_date=selected_date,
                selected_time_start__lt=selected_time_end,
                selected_time_end__gt=selected_time_start,
            ).exists()
            
            if existing_booking:
                form.add_error(None, "Дублирующийся заказ уже существует для выбранной даты и времени.")
            else:
                try:
                    booking.full_clean()  # Проверяем валидность модели
                    booking.save()
                    return redirect('profile')  # Перенаправляем на страницу успешного создания заказа
                except ValidationError:
                    form.add_error(None, "Некорректные данные бронирования.")
    else:
        form = BookingForm()

    context['form'] = form
    return render(request, 'field_app/create_booking.html', context)



def profile(request):
    user = request.user
    bookings = Booking.objects.filter(owner__user=user)
    fields = Field.objects.filter(owner__user=user)
    try:
        owner = Owner.objects.get(user=user)
    except Owner.DoesNotExist:
        owner = None
        
    context = {
        'user': user,
        'bookings': bookings,
        'fields': fields,
        'owner': owner
    }
    
    return render(request, 'field_app/profile.html', context)

def owner_detail(request):
    user = request.user
    try:
        owner = Owner.objects.get(user=user)
    except Owner.DoesNotExist:
        owner = None

    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.user = user
            owner.save()
            return redirect('profile')  # Перенаправьте на страницу с данными владельца

    else:
        form = OwnerForm(instance=owner)

    return render(request, 'field_app/owner_detail.html', {'form': form, 'owner': owner})


# def field_detail(request, pk):
#     field = get_object_or_404(Field, pk=pk)
#     time_slots = [
#         "00:00 - 00:30",
#         "00:30 - 01:00",
#         "01:00 - 01:30",
#         "01:30 - 02:00",
#         "02:00 - 02:30",
#         "02:30 - 03:00",
#         "03:00 - 03:30",
#         "03:30 - 04:00",
#         "04:00 - 04:30",
#         "04:30 - 05:00",
#         "05:00 - 05:30",
#         "05:30 - 06:00",
#         "06:00 - 06:30",
#         "06:30 - 07:00",
#         "07:00 - 07:30",
#         "07:30 - 08:00",
#         "08:00 - 08:30",
#         "08:30 - 09:00",
#         "09:00 - 09:30",
#         "09:30 - 10:00",
#         "10:00 - 10:30",
#         "10:30 - 11:00",
#         "11:00 - 11:30",
#         "11:30 - 12:00",
#         "12:00 - 12:30",
#         "12:30 - 13:00",
#         "13:00 - 13:30",
#         "13:30 - 14:00",
#         "14:00 - 14:30",
#         "14:30 - 15:00",
#         "15:00 - 15:30",
#         "15:30 - 16:00",
#         "16:00 - 16:30",
#         "16:30 - 17:00",
#         "17:00 - 17:30",
#         "17:30 - 18:00",
#         "18:00 - 18:30",
#         "18:30 - 19:00",
#         "19:00 - 19:30",
#         "19:30 - 20:00",
#         "20:00 - 20:30",
#         "20:30 - 21:00",
#         "21:00 - 21:30",
#         "21:30 - 22:00",
#         "22:00 - 22:30",
#         "22:30 - 23:00",
#         "23:00 - 23:30",
#         "23:30 - 24:00"
#     ]
#     context = {
#         'field': field,
#         'time_slots': time_slots
#     }
#     return render(request, 'field_app/field_detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Field, TimeSlot

from datetime import date, timedelta

def field_detail(request, pk):
    field = get_object_or_404(Field, pk=pk)
    time_slots = [
        "00:00 - 00:30",
        "00:30 - 01:00",
        "01:00 - 01:30",
        "01:30 - 02:00",
        "02:00 - 02:30",
        "02:30 - 03:00",
        "03:00 - 03:30",
        "03:30 - 04:00",
        "04:00 - 04:30",
        "04:30 - 05:00",
        "05:00 - 05:30",
        "05:30 - 06:00",
        "06:00 - 06:30",
        "06:30 - 07:00",
        "07:00 - 07:30",
        "07:30 - 08:00",
        "08:00 - 08:30",
        "08:30 - 09:00",
        "09:00 - 09:30",
        "09:30 - 10:00",
        "10:00 - 10:30",
        "10:30 - 11:00",
        "11:00 - 11:30",
        "11:30 - 12:00",
        "12:00 - 12:30",
        "12:30 - 13:00",
        "13:00 - 13:30",
        "13:30 - 14:00",
        "14:00 - 14:30",
        "14:30 - 15:00",
        "15:00 - 15:30",
        "15:30 - 16:00",
        "16:00 - 16:30",
        "16:30 - 17:00",
        "17:00 - 17:30",
        "17:30 - 18:00",
        "18:00 - 18:30",
        "18:30 - 19:00",
        "19:00 - 19:30",
        "19:30 - 20:00",
        "20:00 - 20:30",
        "20:30 - 21:00",
        "21:00 - 21:30",
        "21:30 - 22:00",
        "22:00 - 22:30",
        "22:30 - 23:00",
        "23:00 - 23:30",
        "23:30 - 24:00"
    ]
    
    # Формирование словаря availability
    availability = {}
    current_date = date.today()
    for i in range(7):  # 7 дней вперед
        date_str = str(current_date)
        time_slots_for_date = []

        # Получение занятых слотов для текущей даты
        time_slots_for_date = field.time_slots.filter(start_time__date=current_date).values_list('start_time', flat=True)

        availability[date_str] = time_slots_for_date
        current_date += timedelta(days=1)

    context = {
        'field': field,
        'availability': availability,
        'time_slots': time_slots
    }
    return render(request, 'field_app/field_detail.html', context)




def main(request):
    fields = Field.objects.prefetch_related('photos__photo').all()
    return render(request, 'field_app/main.html', {'fields': fields})






@login_required
def add_field(request):
    owner, created = Owner.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = FieldForm(request.POST, request.FILES)
        if form.is_valid():
            field = form.save(commit=False)
            field.owner = owner

            # Сохраняем фото в папку "fields"
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                field.photo.save(photo.name, photo)

            field.save()

            # Вывод информации
            print("Сохраненный путь к фото:", field.photo.path)
            print("URL фото:", field.photo.url)
            print("Абсолютный путь к папке media:", settings.MEDIA_ROOT)

            return redirect('profile')
    else:
        form = FieldForm()

    return render(request, 'field_app/add_field.html', {'form': form})

# def field_detail(request, pk):
#     field = Field.objects.get(pk=pk)
#     time_slots = field.time_slots.all()

#     context = {
#         'field': field,
#         'time_slots': time_slots,
#     }

#     return render(request, 'field_app/field_detail.html', context)
