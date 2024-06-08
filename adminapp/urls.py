from django.urls import path
from . import views
from adminapp.main import home_page,about,contact_page 

urlpatterns = [
    path('',home_page,name='home_page'),
    path('about/',about ,name='about'),
    path('contact/',contact_page,name='contact_page'),

    path('admin-login/',views.admin_login,name='admin-login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
   
    path('add-parking-slot',views.add_parking_slots,name='add_slot'),
    path('manage_slots',views.manage_parking_slots,name='manage_slots'),
    path('update_slot/<int:id>/',views.update_slot,name='update_slot'),
    path('delete-slot/<int:id>/',views.delete_slot,name="delete_slot"),
    path('all_bookings/',views.all_bookings,name="all_bookings"),
    path('view_feedback/',views.view_feedback,name='view_feedback'),
    path('feedback/',views.feedback_analysis,name='feedback_analysis'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),


]
