from django.urls import path
from .views import (
    PatientCreateView, PatientUpdateView, PatientDeleteView, 
    VaccinationRecordCreateView, VaccinationRecordUpdateView, VaccinationRecordDeleteView
)

from .views import PrescriptionUploadView, PersonalUploadView,PrescriptionDeleteView,PersonalDeleteView,PersonalMediaListView, PrescriptionMediaListView


app_name = 'profiles'  # Namespace for profiles app

urlpatterns = [
    path('create/', PatientCreateView.as_view(), name='patient-create'),  # Create a new pet profile
    path('update/<int:pk>/', PatientUpdateView.as_view(), name='patient-update'),  # Update a pet profile by its primary key (pk)
    path('delete/<int:pk>/', PatientDeleteView.as_view(), name='patient-delete'),  # Delete a pet profile by its pk

    # Vaccination record URLs
   path('profiles/<int:pk>/vaccinations/create/', VaccinationRecordCreateView.as_view(), name='vaccinationrecord-create'),

    path('vaccination/<int:pk>/update/', VaccinationRecordUpdateView.as_view(), name='vaccinationrecord-update'),  # Update a vaccination record
    path('vaccination/<int:pk>/delete/', VaccinationRecordDeleteView.as_view(), name='vaccinationrecord-delete'),
    path('upload/prescription/', PrescriptionUploadView.as_view(), name='prescription_upload'),

    path('media/prescription/', PrescriptionMediaListView.as_view(), name='prescription_media_list'),
  
    path('media/prescription/delete/<int:pk>/', PrescriptionDeleteView.as_view(), name='prescription_delete'),

]


