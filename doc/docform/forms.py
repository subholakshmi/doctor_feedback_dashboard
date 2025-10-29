from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor, Patient, PatientUpdate
import json


class DoctorSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    mobile_number = forms.CharField(max_length=20, required=True)
    email_address = forms.EmailField(required=False)
    specialty = forms.CharField(max_length=255, required=True)
    years_of_practice = forms.IntegerField(required=True, min_value=0)
    hospital_name = forms.CharField(max_length=255, required=True)
    city_location = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Use your mobile number as username'
        
        # Add CSS classes for better styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password1':
                field.help_text = 'At least 8 characters'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                mobile_number=self.cleaned_data['mobile_number'],
                email_address=self.cleaned_data.get('email_address'),
                specialty=self.cleaned_data['specialty'],
                years_of_practice=self.cleaned_data['years_of_practice'],
                hospital_name=self.cleaned_data['hospital_name'],
                city_location=self.cleaned_data['city_location']
            )
        return user


class PatientForm(forms.ModelForm):
    conditions_treated = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter conditions separated by commas (e.g., Diabetes, Hypertension, Obesity)"
    )

    class Meta:
        model = Patient
        fields = [
            'product_name', 'disease_name', 'conditions_treated',
            'biochemistry_data', 'medical_investigation', 
            'improvements_observed', 'before_image', 'after_image'
        ]
        widgets = {
            'disease_name': forms.Textarea(attrs={'rows': 3}),
            'biochemistry_data': forms.Textarea(attrs={'rows': 4}),
            'medical_investigation': forms.Textarea(attrs={'rows': 4}),
            'improvements_observed': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['before_image', 'after_image']:
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control-file'


class PatientUpdateForm(forms.ModelForm):
    update_data = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8}),
        help_text='Enter update data as JSON. Example: {"date": "2025-10-28", "improvements": "Significant improvement", "notes": "Patient responding well"}'
    )

    class Meta:
        model = PatientUpdate
        fields = ['update_data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['update_data'].widget.attrs['class'] = 'form-control'

    def clean_update_data(self):
        data = self.cleaned_data['update_data']
        try:
            # Validate JSON format
            json_data = json.loads(data)
            return json_data
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format. Please check your syntax.")