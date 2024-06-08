from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages

from .models import AddParkingSlots
from django.core.paginator import Paginator
from userapp.models import BookingSlots,UserFeedback,UserModel
from datetime import datetime


# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin':
            messages.success(request,'Admin Logined successfully ')
            return redirect('admin_dashboard')
        else:
            messages.success(request,'Invalid username and password ')
            return redirect('admin-login')
    return render(request, 'admin/admin-login.html')

def admin_dashboard(request):
    date = datetime.today()
    
    # owners = BookingSlots.objects.filter(user__user_id=user).count()
    slots = AddParkingSlots.objects.all().count()
    bookings = BookingSlots.objects.filter(parking_date=date).count()
    # vehicles = BookingSlots.objects.filter(status='checkIn').count()

    context = {
        'bookings':bookings,
        'slots':slots,
        # 'vehicles':vehicles,
        # 'owners':owners
    }
 
    return render(request, 'admin/admin-dashboard.html',context)



def add_parking_slots(request):
    if request.method == 'POST':
        location_name = request.POST.get('location')
        phone_number = request.POST.get('phone_number')
    
        total_slots = request.POST.get('total')
        available_slots = request.POST.get('slots')
     
        session = request.POST.get('session')
        booking_start_time = request.POST.get('start_time')
        booking_end_time  = request.POST.get('end_time')
        pin = request.POST.get('pin')

        try:
            AddParkingSlots.objects.create(
                location = location_name,
                phone_number = phone_number,
                total_slots = total_slots,
                available_slots  = available_slots,
                parking_session = session,
                booking_start_time = booking_start_time,
                booking_end_time = booking_end_time,
                pin_number = pin
            )

            messages.success(request, 'Slot Added successfully')
            return redirect('add_slot')
            
        except:
            messages.error(request,"Failed to Add Slot")
            return redirect('add_slot')          
    return render(request,'admin/admin-addParkingSlot.html') 

def manage_parking_slots(request):
    slots = AddParkingSlots.objects.all().order_by('-slot_id')

    paginator = Paginator(slots,4)
    page_number = request.GET.get('page')
    parking_slots = paginator.get_page(page_number)

    context = {
        'parking_slots':parking_slots
    }

    return render(request,'admin/admin-manageParkingSlots.html',context)

def update_slot(request,id):
    slot = AddParkingSlots.objects.get(slot_id=id)
    update = get_object_or_404(AddParkingSlots,slot_id=id)

    if request.method =='POST':
        location_name = request.POST.get('location')
        number = request.POST.get('number')
        total_slots = request.POST.get('slots')
        # available_slots = request.POST.get('available_slots')
        # booked_slots = request.POST.get('booked_slots')
        session = request.POST.get('parking_session')
        booking_start_time = request.POST.get('start_time')
        booking_end_time = request.POST.get('end_time')
        pin = request.POST.get('pin_number')
        Parking_charges = request.POST.get('parking_charge')

        slots = int(total_slots) - slot.booked_slots
        print(total_slots,'total slots')
        print(slot.booked_slots,'booked slots')
        print(slots,'ssssssssssssssss')

        update.location = location_name
        update.phone_number = number
        update.total_slots = total_slots
        update.available_slots = slots
        
        update.parking_session = session
        update.booking_start_time = booking_start_time
        update.booking_end_time = booking_end_time
        update.pin_number = pin
        update.parking_charge = Parking_charges

        update.save()
        messages.success(request,'ParkingSlot Updated successfully')
        return redirect('update_slot',id=id)


    context = {
        "slot":slot
    }
    return render(request,'admin/admin-parkingupdate.html',context)

def delete_slot(request,id):
    slot = AddParkingSlots.objects.get(pk=id)
    slot.delete()
    messages.success(request,'Slot removed successfully')
    return redirect('manage_slots')

def all_bookings(request):
    bookings =  BookingSlots.objects.all().order_by('-booking_id')

    context = {
        'all_bookings':bookings
    } 

    return render(request,'admin/booking_details.html',context)

def view_feedback(request):
    feedback = UserFeedback.objects.all().order_by('-feedback_id')
    for i in feedback:
      
        print(type(i.booking_experience)) 
    context = {
        'feedback':feedback
    }
    return render(request,'admin/admin-viewFeedbacks.html',context)

def feedback_analysis(reqeust):
    very_positive = UserFeedback.objects.filter(feedback_sentiment='very Positive').count()
    positive = UserFeedback.objects.filter(feedback_sentiment='Positive').count()
    very_negetive = UserFeedback.objects.filter(feedback_sentiment='very Negative').count()
    negetive = UserFeedback.objects.filter(feedback_sentiment='Negative').count()
    neutral = UserFeedback.objects.filter(feedback_sentiment='Neutral').count()

    context = {
        'very_positive':very_positive,
        'positive':positive,
        'very_negetive':very_negetive,
        'negetive':negetive,
        'neutral':neutral
    }
    return render(reqeust,'admin/admin-feedbackAnalysis.html',context)

def admin_logout(request):
    messages.success(request,'Admin logout successfully')
    return redirect('home_page')