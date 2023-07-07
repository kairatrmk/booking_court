from django import template

register = template.Library()

@register.filter
def total_bill(bookings):
    return sum(booking.total_bill for booking in bookings)
