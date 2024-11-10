f"""rom rest_framework import generics
from .models import Patient, VaccinationRecord
from .serializers import PatientSerializer, VaccinationRecordSerializer

# API View for Patient
class PatientListCreate(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# API View for VaccinationRecord (if needed)
class VaccinationRecordListCreate(generics.ListCreateAPIView):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer

class VaccinationRecordRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializer"""
