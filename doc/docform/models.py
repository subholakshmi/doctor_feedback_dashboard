import uuid
from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20, unique=True)
    email_address = models.EmailField(blank=True, null=True)
    specialty = models.CharField(max_length=255)
    years_of_practice = models.IntegerField()
    hospital_name = models.CharField(max_length=255)
    city_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.full_name} - {self.specialty}"

    class Meta:
        db_table = 'doctors'


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')
    product_name = models.CharField(max_length=255)
    disease_name = models.TextField()
    conditions_treated = models.TextField(help_text="Enter conditions separated by commas")
    biochemistry_data = models.TextField()
    medical_investigation = models.TextField()
    improvements_observed = models.TextField()
    before_image = models.ImageField(upload_to='patients/before/', blank=True, null=True)
    after_image = models.ImageField(upload_to='patients/after/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patient {self.id} - {self.disease_name}"

    def get_conditions_list(self):
        """Return conditions as a list"""
        if self.conditions_treated:
            return [c.strip() for c in self.conditions_treated.split(',')]
        return []

    class Meta:
        db_table = 'patients'
        ordering = ['-created_at']


class PatientUpdate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='updates')
    update_data = models.JSONField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for Patient {self.patient.id} - {self.updated_at}"

    class Meta:
        db_table = 'patient_updates'
        ordering = ['-updated_at']