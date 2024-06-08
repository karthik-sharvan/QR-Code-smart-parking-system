from django.shortcuts import render,redirect

def home_page(request):
    return render(request,'admin/home.html')

def about(request):
    return render(request,'admin/about-us.html')

def contact_page(request):
    return render(request,'admin/contact-us.html')