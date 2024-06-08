from django.db import models
import qrcode
from io import BytesIO
from PIL import Image
from django.core.files import File
from adminapp.models import AddParkingSlots

# Create your models here.

class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=200)
    vehicle_number = models.CharField(max_length=300)
    license_number = models.CharField(max_length=300)
    profile = models.ImageField(upload_to='images/')

    class Meta:
        db_table = 'user_details'

class BookingSlots(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user= models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True)
    slot = models.ForeignKey(AddParkingSlots,on_delete=models.CASCADE,null=True)
    parking_date = models.DateField(max_length=100)
    in_time = models.DateTimeField(null=True)
    out_time = models.DateTimeField(null=True)
    total_parking_time =models.CharField(null=True,max_length=1000) 
    total_charges = models.IntegerField(default=0,null=True)
    status = models.CharField(max_length=100,default='checkIn',null=True)
    

    class Meta:
        db_table = 'booking_slots'

class UserFeedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    slot = models.ForeignKey(BookingSlots,on_delete=models.CASCADE)
    comment = models.TextField()
    feedback_sentiment = models.CharField(max_length=100)
    booking_experience = models.IntegerField()

    class Meta:
        db_table = "User-Feedback"

    




