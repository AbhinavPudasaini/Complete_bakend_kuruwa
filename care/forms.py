from django import forms
from .models import Caretaker, Patient

class CaretakerSignupForm(forms.ModelForm):
    # confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Caretaker
        fields = ['full_names', 'emails', 'phone_numbers', 'specializations','experiences', 'citys','availability', 'rate', 'passwords', 'image']
        widgets = {
            'passwords': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        passwords = cleaned_data.get("passwords")
        # confirm = cleaned_data.get("confirm_password")
        # if password != confirm:
        #     raise forms.ValidationError("Passwords do not match.")

class PatientSignupForm(forms.ModelForm):
    # confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Patient
        fields = ['full_name', 'email', 'phone_number', 'city', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        # confirm = cleaned_data.get("confirm_password")
        # if password != confirm:
        #     raise forms.ValidationError("Passwords do not match.")
