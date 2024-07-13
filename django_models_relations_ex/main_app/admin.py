from django.contrib import admin

from main_app.models import Car


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'year', 'owner', 'car_details')

    @staticmethod
    def car_details(obj: object):
        try:
            name = obj.owner.name
        except AttributeError:
            name = 'No owner'


        try:
            reg_num = obj.registration.registration_number
        except AttributeError:
            reg_num = 'No registration number'

        return f"Owner: {name}, Registration: {reg_num}"

    car_details.short_description = "Car Details"