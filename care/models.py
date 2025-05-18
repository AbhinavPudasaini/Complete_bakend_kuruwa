from django.db import models
from django.contrib.auth.models import User

class Caretaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True, blank=True)
    full_names = models.CharField(max_length=100)
    emails = models.EmailField(unique=True)
    phone_numbers = models.CharField(max_length=15)
    specializations = models.CharField(max_length=100, default="Beginner")
    experiences = models.IntegerField()  # in years
    citys = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    passwords = models.CharField(max_length=128)  # We'll hash this manually or later use User model
    image = models.ImageField(upload_to='caretaker_images/')

    def __str__(self):
        return self.full_names

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.full_name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    
    caretaker = models.ForeignKey(Caretaker, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, default=None)
    patient_location = models.CharField(max_length=255)
    book_date = models.DateField(default=None)
    requested_at = models.TimeField(auto_now_add=True)
    duration = models.IntegerField(default=1)  # in hours
    Description = models.CharField(max_length=50, default="No description")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Booking from {self.patient.username} to {self.caretaker.full_names} - {self.status}"