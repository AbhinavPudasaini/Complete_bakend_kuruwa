from django.shortcuts import render, redirect
from .forms import CaretakerSignupForm, PatientSignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from care.models import Caretaker, Patient
from django.contrib.auth.decorators import login_required


from django.contrib import messages

def caretaker_signup(request):
    if request.method == 'POST':
        form = CaretakerSignupForm(request.POST, request.FILES)

        if form.is_valid():


            email = form.cleaned_data['emails']
            raw_password = form.cleaned_data['passwords']
                
            user = User.objects.create_user(
                    username=email,
                    password=raw_password  # Automatically hashed
                )

                # Create Caretaker instance linked to User
            caretaker = form.save(commit=False)
            caretaker.availability = True 
            caretaker.user = user
            caretaker.save()
            return redirect('/') 
        else:
            print(form.errors) # redirect to login page
    else:
        form = CaretakerSignupForm()
    return render(request, 'login.html', {'form': form})

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():


            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password']
                
            user = User.objects.create_user(
                    username=email,
                    password=raw_password  # Automatically hashed
                )

                # Create Caretaker instance linked to User
            patient = form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('/')
    
        else:
            print(form.errors)
    else:
        form = PatientSignupForm()
    return render(request, 'login.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not User.objects.filter(username = email).exists():
            messages.info(request, "Username doesn't exists.")
            return redirect('/login/')
        
        user = authenticate(request, username=email, password=password)  # We used email as username
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('/')  # redirect to a dashboard or home page
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')

def profile_update(request):
    if request.method == 'POST':
        form = CaretakerSignupForm(request.POST, instance=request.user.caretaker)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('/profile_update/')
    else:
        form = CaretakerSignupForm(instance=request.user.caretaker)
    return render(request, 'profile_update.html', {'form': form})

def caretaker_list_view(request):
    caretakers = Caretaker.objects.all().order_by('-availability')  # Sort by availability
    return render(request, 'Browse_caregiver.html', {'caretakers': caretakers})

def about(request):
    return render(request, 'About.html')

def home(request):
    return render(request, 'Home.html')

def about(request):
    return render(request, 'About.html')

def contact(request):
    return render(request, 'Contact_Us.html')  

def price(request):
    return render(request, 'Pricing.html')

# def browse(request):
#     return render(request, 'Browse_caregiver.html')

# def login(request):
#     return render(request, 'login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')

def notification(request):
    return render(request, 'notification.html')

# def book(request):
#     return render(request, 'book.html')

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Caretaker, Booking
from django.utils import timezone

@login_required
def book_caretaker(request, caretaker_id):
    caretaker = get_object_or_404(Caretaker, id=caretaker_id)

    if not caretaker.availability:
        messages.error(request, "This caretaker is currently unavailable.")
        return redirect('home')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        location = request.POST.get('location')
        book_date = request.POST.get('book_date')  # should be in yyyy-mm-dd format
        time = request.POST.get('time')  # should be in HH:MM format
        duration = request.POST.get('duration')  # in hours
        description = request.POST.get('desc')

        if not all([full_name, phone_number, location, book_date]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'book.html', {'caretaker': caretaker})

        Booking.objects.create(
            caretaker=caretaker,
            patient=request.user,
            patient_full_name=full_name,
            phone_number=phone_number,
            patient_location=location,
            book_date=book_date,
            requested_at=time,
            duration=duration,
            Description=description
        )

        messages.success(request, "Booking request sent successfully!")
        return redirect('home')  # or a confirmation page

    return render(request, 'book.html', {'caretaker': caretaker})


from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings



# @require_POST
@login_required
def respond_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # if booking.caretaker.user != request.user:
    #     return HttpResponseForbidden("You are not authorized.")

    response = request.POST.get('response')

    if response == "Accept":
        booking.status = "Accepted"
        booking.save()
        booking.caretaker.availability = False
        booking.caretaker.save()
        Caretaker.objects.filter(id=booking.caretaker.id).update(availability=False)

        send_mail(
                subject='Your Booking has been Accepted ✅',
                message=f'Hello {booking.patient_full_name},\n\nYour booking with {booking.caretaker.full_names} has been accepted.\nDate: {booking.book_date}\nLocation: {booking.patient_location}\n\nThank you!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.patient.email],
                fail_silently=True,)

        # Notify patient via message or email (optional)
        messages.success(request, f"You accepted the booking request from {booking.patient_full_name}.")
    elif response == "Decline":
        booking.status = "Declined"
        booking.save()
        messages.info(request, f"You declined the booking request.")
        send_mail(
                subject='Your Booking has been declined ',
                message=f'Hello {booking.patient_full_name},\n\nYour booking with {booking.caretaker.full_names} has been declined.\nDate: {booking.book_date}\nLocation: {booking.patient_location}\n\nThank you!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.patient.email],
                fail_silently=True,)


    return render(request, 'notification.html', {'booking': booking})

@login_required
def notifications(request):
    # Assuming request.user is the caretaker or linked to caretaker
    caretaker = get_object_or_404(Caretaker, user=request.user)
    bookings = Booking.objects.filter(caretaker=caretaker, status="Pending").order_by('-requested_at')

    return render(request, 'notification.html', {'bookings': bookings})

