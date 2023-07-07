from django import template

register = template.Library()

@register.filter
def get_booking_status(time_slot):
    if time_slot.is_booked:
        return "Занято"
    else:
        return "Свободно"

