from django import forms
from django.contrib.auth.models import User
from .models import Profile, HealthEntry
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)
    height = forms.FloatField(required=True, help_text="Height in centimeters (cm)")
    weight = forms.FloatField(required=True, help_text="Weight in kilograms (kg)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'height', 'weight']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                age=self.cleaned_data['age'],
                height=self.cleaned_data['height'],
                weight=self.cleaned_data['weight']
            )
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'height', 'weight']

class HealthEntryForm(forms.ModelForm):
    class Meta:
        model = HealthEntry
        fields = ['date', 'disorder', 'required_medicine', 'medicine_time_table', 'doctor_name', 'doctor_contact']

