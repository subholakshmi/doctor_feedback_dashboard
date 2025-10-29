from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Doctor, Patient, PatientUpdate
from .forms import DoctorSignUpForm, PatientForm, PatientUpdateForm


def signup_view(request):
    """Handle doctor signup"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Doctor Feedback.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DoctorSignUpForm()
    
    return render(request, 'doctors/signup.html', {'form': form})


def login_view(request):
    """Handle doctor login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'doctors/login.html', {'form': form})


def logout_view(request):
    """Handle doctor logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Display doctor's dashboard with all patients"""
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('login')
    
    patients = Patient.objects.filter(doctor=doctor)
    
    context = {
        'doctor': doctor,
        'patients': patients,
        'total_patients': patients.count(),
    }
    return render(request, 'doctors/dashboard.html', context)


@login_required
def add_patient_view(request):
    """Add a new patient"""
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('login')
    
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.doctor = doctor
            patient.save()
            messages.success(request, 'Patient added successfully!')
            return redirect('patient_detail', patient_id=patient.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientForm()
    
    return render(request, 'doctors/add_patient.html', {'form': form, 'doctor': doctor})


@login_required
def patient_detail_view(request, patient_id):
    """View patient details and updates"""
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('login')
    
    patient = get_object_or_404(Patient, id=patient_id, doctor=doctor)
    updates = PatientUpdate.objects.filter(patient=patient)
    
    context = {
        'doctor': doctor,
        'patient': patient,
        'updates': updates,
        'conditions': patient.get_conditions_list(),
    }
    return render(request, 'doctors/patient_detail.html', context)


@login_required
def add_update_view(request, patient_id):
    """Add an update to a patient's record"""
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('login')
    
    patient = get_object_or_404(Patient, id=patient_id, doctor=doctor)
    
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.patient = patient
            update.save()
            messages.success(request, 'Patient update added successfully!')
            return redirect('patient_detail', patient_id=patient.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientUpdateForm()
    
    context = {
        'doctor': doctor,
        'patient': patient,
        'form': form,
    }
    return render(request, 'doctors/add_update.html', context)


def home_view(request):
    """Home page - redirect to login or dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')