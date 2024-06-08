from django.urls import path
from . import views

urlpatterns = [
   
    path('user_register/',views.user_registration,name='registration'),
    path('user-login/',views.user_login,name='user_login'),
    path('user_dashboard/',views.user_dashboard,name="user_dashboard"),
    path('book_slot/',views.user_booking_slot,name="book_slot"),
    path('slot/<int:id>/',views.book_slot,name="bookSlot"),
    path('my_bookings/',views.my_bookings,name="bookings"),
    path('check_out/<int:id>/',views.ckeck_out,name="check_out"),
    path('payment/<int:id>/',views.payment_details,name='payment'),
    path('pay/<int:id>/',views.status_success,name='pay'),
    path('booking_history/',views.booking_history,name="booking_history"),
    
    path('user_profile/',views.user_profile,name='user-profile'),
    path('feedback/<int:id>/',views.user_feedback,name='feedback'),
    path('user_logout/',views.user_logout,name='user_logout'),
    
]
