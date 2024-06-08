from django.shortcuts import render,redirect,get_object_or_404

from .models import UserModel,BookingSlots,UserFeedback
from django.contrib import messages
from adminapp.models import AddParkingSlots
from datetime import datetime,date,timedelta
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import math
from textblob import TextBlob
import requests
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from smart_parking.settings import DEFAULT_FROM_EMAIL
import random

# Create your views here.


           
def user_registration(request):

    if request.method == "POST" and 'profile' in request.FILES:
        full_name = request.POST.get('name')

        email = request.POST.get('email')
        # password = request.POST.get('password')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_number = request.POST.get('vehicle_number')
        license_number = request.POST.get('license_number')
        profile = request.FILES['profile']

        chars = '01234567899876543210112233445566778899ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        user_password = get_random_string(8, chars)
        print(user_password,'user password')
          
        try:
            UserModel.objects.get(email=email)
            messages.info(request,'Email Already exists')
            return redirect('registration')
        except:
            data= UserModel.objects.create(
                full_name = full_name,
                email = email,
                password = user_password,
                phone = phone,
                city = city,
                vehicle_type = vehicle_type,
                vehicle_number = vehicle_number,
                license_number = license_number,
                profile = profile
            )
           


        mail =data.email
        html_content = f'Dear Customer,Your Login Password is :{data.password}' 
        from_mail = DEFAULT_FROM_EMAIL
        to_mail = [mail]

        try:
            print(mail)
            message = EmailMultiAlternatives('Authentication Password is',html_content,from_mail,to_mail)
            message.attach_alternative(html_content, 'text/html')
            if message.send():
                print(message)
                # messages.success(request,'password sent successfully')

        except:
                messages.error(request, 'there is a problem try again ')
                # return redirect('registration')  
         
    
        print(user_password,'this')
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        # create a dictionary
        my_data = {
            'sender_id': 'FSTSMS', 
            'message': 'Dear Developer,Your Authentication Password is :'+str(data.password), 
            'language': 'english', 
            'route': 'q', 
            'numbers':data.phone,
        }
        
        print(my_data,'l')
            # create a dictionary
        headers = {
                'authorization': "RiE8PuQDhbLnUkKe43p5vHsta0dFTyqcoNS7xrAwC9zO2WjgVG875H0JStiefd23jxPM4aLVzrEYmvOI",
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache"
        }
            # make a post request
        response = requests.request("POST",
                                url,
                                data = my_data,
                                headers = headers)

        
        print(response.text,'hi') 
        messages.success(request,'User Register Successfully')
        return redirect('user_login')
    return render(request, 'user/user-register.html')

    
def user_login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password,"lknvlsdvlnvsvkdsv")

        try:
           
            user = UserModel.objects.get(email=email,password=password)
            request.session['user_id']=user.user_id
            messages.success(request,'User Logined successfully')
            return redirect('user_dashboard')
        except:
            messages.error(request,'Login Failed try again')
            return redirect('user_login')

    else: 
        return render(request,'user/user-login.html')


def user_dashboard(request):
    return render(request,'user/user-dashboard.html')



def user_booking_slot(request):
    slot = AddParkingSlots.objects.all().order_by('-slot_id')
    context = {

        "slots":slot
    }
    return render(request,'user/user-bookslot.html',context)


def book_slot(request,id):
    user_id = request.session['user_id']
    user = UserModel.objects.get(user_id=user_id)
    parking_slot = AddParkingSlots.objects.get(pk=id)

    in_time = timezone.now()
    print(in_time,'in time444444')
    date_of_parking = date.today()

    try:
        BookingSlots.objects.create(
            user = user,
            slot = parking_slot,
            parking_date = date_of_parking,
            in_time = in_time,    
        )

        parking_slot.booked_slots += 1
        parking_slot.available_slots -=1

        parking_slot.save()

        messages.success(request,'Parking Slot Booked successfully')
        return redirect('book_slot')

    except:
        messages.error(request,'Failed to Book Parking Slot')
        return redirect('book_slot')


def my_bookings(request):
    user_id = request.session['user_id']
    bookings = BookingSlots.objects.filter(user__user_id=user_id,status='checkIn').order_by('-booking_id')


    context = {
        'bookings':bookings
    }
    return render(request,'user/user-mybookings.html',context)

def ckeck_out(request,id):
    user_id = request.session['user_id']
    user = UserModel.objects.get(user_id=user_id)
    booking_slot = BookingSlots.objects.get(pk=id)
    parking_slot = AddParkingSlots.objects.get(pk=booking_slot.slot.slot_id)
  
    out_time = timezone.now()

    try:
        booking_slot.out_time = out_time
        booking_slot.save()
        In = booking_slot.in_time
        out = booking_slot.out_time
        time = out - In
        
        print(time.total_seconds(),'total seconds')
        print(time.total_seconds()/60,'minutes')
        cost = time.total_seconds()/60
        
        h = math.ceil(cost/60)
        print(h,'total hours')
        total_charges = h*parking_slot.parking_charge
        print(h*50,'oioioi')
        print(h*50)
     
        booking_slot.total_charges = total_charges
        booking_slot.total_parking_time = h
    
        booking_slot.save()
        booking_slot.slot.qr_code.delete()
        parking_slot.booked_slots -=1
        parking_slot.available_slots +=1
        parking_slot.save()

        return redirect('payment',id=id)

    except:
        print('vkvkvkvkvkvk')
        messages.success(request,'Failed to Check Out')
        return redirect('bookings')
    

def payment_details(request,id):
    booking_slot = BookingSlots.objects.get(pk=id)
    # parking_slot = AddParkingSlots.objects.get(pk=booking_slot.slot.slot_id)

    context = {
        'booking_slot':booking_slot,
        
    }

    return render(request,'user/payment_details.html',context)

def status_success(request,id):
    booking_slot = BookingSlots.objects.get(pk=id)
    if request.method == "POST":
        booking_slot.status = 'check_out'
        booking_slot.save()
        messages.success(request,'Payment Done Successfully')
        return redirect('bookings')

def booking_history(request):
    user_id = request.session['user_id']
    history = BookingSlots.objects.filter(status='check_out').order_by('-booking_id').filter(user__user_id=user_id)

    context = {
        'booking_history':history
    }
    return render(request,'user/booking_history.html',context) 
  
def user_profile(request):
    id = request.session['user_id']
    user = UserModel.objects.get(user_id = id)
    if request.method == 'POST' :
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        city = request.POST.get('city')
        vehical = request.POST.get('vehicle')
        vehicle_number = request.POST.get('vehicle_number')
        license_number = request.POST.get('licence_number')
       

        if not request.FILES.get('profile',False):
            user.full_name = name
            user.email = email
            user.phone = number
            user.city = city
            user.vehicle_type = vehical
            user.vehicle_number = vehicle_number
            user.license_number = license_number

        if request.FILES.get('profile',False):
            profile = request.FILES['profile']
            user.full_name = name
            user.email = email
            user.phone = number
            user.city = city
            user.vehicle_type = vehical
            user.vehicle_number = vehicle_number
            user.license_number = license_number
            user.profile = profile

        user.save()
        messages.success(request,'Profile updated successfully')
        return redirect('user-profile')
       
    context = {
        "user":user
    }
    return render(request,'user/user-myprofile.html',context)

def user_feedback(request,id):
    user_id = request.session['user_id']
    user = UserModel.objects.get(pk=user_id) 

    slot = BookingSlots.objects.get(pk=id)

    if request.method == 'POST':
        rating = request.POST.get('stars')
        feedback = request.POST.get('feedback')

        if not request.POST.get('stars'):
            messages.info(request,"Please rate for Parking Slots")
            return redirect('feedback')
    
        if not request.POST.get('feedback'):
            messages.info(request,"Enter Your Feedback")
            return redirect('feedback')

        analysis = TextBlob(feedback)

        sentement = ''
        if analysis.polarity >=0.5:
            sentement = 'very Positive'
        elif analysis.polarity > 0 and analysis.polarity < 0.5 :
            sentement = 'Positive'
        elif analysis.polarity <= -0.5 :
            sentement='very Negative'
        elif analysis.polarity < 0 and analysis.polarity > -0.5 :
            sentement='Negative'
        else:
            sentement='Neutral'

        UserFeedback.objects.create(
            user = user,
            slot = slot,
            comment = feedback,
            feedback_sentiment = sentement,
            booking_experience = rating
        )
        messages.success(request,'Feedback Send Successfully')
        return redirect('feedback',id=id)
    context = {
        'slot':slot
    }
        
    return render(request,'user/feedback.html',context)

def user_logout(request):
    logout(request)
    messages.success(request,'User Logout Successfully')
    return redirect('home_page')



