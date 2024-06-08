from django.contrib import admin
from .models import UserModel,BookingSlots

# Register your models here.
admin.site.register([UserModel,BookingSlots])
