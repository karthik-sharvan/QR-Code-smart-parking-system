from django.db import models
import qrcode
from io import BytesIO
from PIL import Image
from django.core.files import File
import os

# Create your models here.

class AddParkingSlots(models.Model):
    slot_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    total_slots = models.IntegerField(null=True)
    available_slots = models.IntegerField(null=True)
    booked_slots = models.IntegerField(null=True,default=0)
    parking_session = models.CharField(max_length=100)
    booking_start_time = models.CharField(max_length=100)
    booking_end_time = models.CharField(max_length=100)
    pin_number = models.CharField(max_length=10)
    parking_charge = models.IntegerField(null=True,default=50)
    qr_code = models.ImageField(upload_to='qr_images',null=True)

    def save(self,*args, **kwargs):
        if self.qr_code:
            try:
                    file = str(self.qr_code)
                    os.remove(file)
                    print('success') 
            except:
                    pass
        qr_image = qrcode.make(f'Parking Location :{self.location}\nContect Number :{self.phone_number}\nTotal Slots :{self.total_slots}\nAvailable SLots :{self.available_slots}\nBooked Slots :{self.booked_slots}\nsession :{self.parking_session}\nParking Start Time :{self.booking_start_time}\n Booking End Time :{self.booking_end_time}\n Pin Number :{self.pin_number}\nParking Charges :{self.parking_charge}')
        qr_offset = Image.new('RGB',(500,500),'white')
        qr_offset.paste(qr_image)
        file_name = f'{self.location}_slot_qr.png'
        stream = BytesIO()
        qr_image.save(stream,'PNG')
        self.qr_code.save(file_name,File(stream),save=False)
        qr_offset.close()
        super().save(*args, **kwargs)

    
    class Meta:
        db_table = 'parking_slots'

    def __str__(self):
        return self.location






   

  






