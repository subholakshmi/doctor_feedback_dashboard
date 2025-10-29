from django.contrib import admin
from .models import Doctor, Patient, PatientUpdate


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_number', 'specialty', 'hospital_name', 'city_location', 'created_at')
    list_filter = ('specialty', 'city_location', 'created_at')
    search_fields = ('full_name', 'mobile_number', 'email_address', 'hospital_name')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'product_name', 'disease_name', 'created_at')
    list_filter = ('product_name', 'created_at')
    search_fields = ('disease_name', 'product_name', 'doctor__full_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor')


@admin.register(PatientUpdate)
class PatientUpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('patient__disease_name',)
    readonly_fields = ('id', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('patient', 'patient__doctor')