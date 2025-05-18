from django.urls import path
from . import views

urlpatterns = [
    path('signup/caretaker/', views.caretaker_signup, name='signup_care'),
    path('signup/patient/', views.patient_signup, name='signup_user'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('price/', views.price, name='price'),
    # path('browse/', views.browse, name='browse'),
    path('logout/', views.logout_view, name='logout'),
    path("profile_update/", views.profile_update, name="profile_update"),
path("notification/respond/<int:booking_id>/", views.respond_booking, name="respond_booking"),
    path('browse/', views.caretaker_list_view, name='browse'),
    # path('book/', views.book, name='book'),
    path('book/<int:caretaker_id>/', views.book_caretaker, name='book'),
    path("notification/", views.notifications, name="notifications"),


# bookings/respond/<int:booking_id>/


    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('logout/', views.logout_view, name='logout'),
]

