from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    height = models.FloatField(help_text="Height in centimeters (cm)")
    weight = models.FloatField(help_text="Weight in kilograms (kg)")
    # Add more fields like blood group, phone, etc., as required.

    def __str__(self):
        return self.user.username

    # Property for calculating BMI
    @property
    def bmi(self):
        if self.height > 0:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return 0

    # Property to determine BMI category
    @property
    def bmi_category(self):
        bmi = self.bmi
        if bmi == 0:
            return "N/A"
        elif bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    # Property to provide healthy eating advice based on BMI
    @property
    def eating_advice(self):
        category = self.bmi_category
        if category == "Underweight":
            return "Eat more frequently, choose nutrient-rich foods, and add healthy calories."
        elif category == "Normal weight":
            return "Maintain a balanced diet rich in fruits, vegetables, and whole grains."
        elif category == "Overweight":
            return "Focus on portion control, eat more fiber, and stay active daily."
        elif category == "Obese":
            return "Adopt a low-calorie, high-nutrient diet and consult a healthcare provider."
        else:
            return "Provide your height and weight to get advice."

class HealthEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    disorder = models.CharField(max_length=255)
    required_medicine = models.CharField(max_length=255)
    medicine_time_table = models.TextField()
    
    # New fields for doctor's information
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    doctor_contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
