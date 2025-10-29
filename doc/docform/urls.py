from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('patient/add/', views.add_patient_view, name='add_patient'),
    path('patient/<uuid:patient_id>/', views.patient_detail_view, name='patient_detail'),
    path('patient/<uuid:patient_id>/update/', views.add_update_view, name='add_update'),
    # NEW ROUTES ADDED
    path('patient/<uuid:patient_id>/edit/', views.edit_patient_view, name='edit_patient'),
    path('patient/<uuid:patient_id>/delete/', views.delete_patient_view, name='delete_patient'),
    path('update/<uuid:update_id>/delete/', views.delete_update_view, name='delete_update'),
]