
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Patient, VaccinationRecord
from .forms import PatientForm, VaccinationRecordForm
from .forms import MediaUploadForm
from .models import MediaUpload
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views import View

# Patient Create View
class PatientCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    model = Patient

    form_class = PatientForm
    template_name = 'profiles/patient_form.html'

    def dispatch(self, request, *args, **kwargs):
       
        if Patient.objects.filter(owner=request.user).exists():
            return redirect('users:show-profile', pk=Patient.objects.get(owner=request.user).pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:show-profile', kwargs={'pk': self.object.pk})


# Patient Update View
class PatientUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    model = Patient
    form_class = PatientForm
    template_name = 'profiles/patient_form.html'

    def get_queryset(self):
        return Patient.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('users:show-profile', kwargs={'pk': self.object.pk})


# Patient List View

# Patient Detail View
class PatientDetailView(LoginRequiredMixin, DetailView):
    login_url = 'users:login'
    model = Patient
    template_name = 'profiles/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vaccination_records'] = VaccinationRecord.objects.filter(patient=self.object)
        return context

    def get_queryset(self):
        return Patient.objects.all()
   

# Patient Delete View
class PatientDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    model = Patient
    template_name = 'profiles/patient_confirm_delete.html'
    success_url = reverse_lazy('users:dashboard')

    def get_queryset(self):
        return Patient.objects.filter(owner=self.request.user)


# VaccinationRecord Create View
class VaccinationRecordCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    model = VaccinationRecord
    form_class = VaccinationRecordForm
    template_name = 'profiles/vaccination_record_form.html'

    def form_valid(self, form):
        patient_profile = get_object_or_404(Patient, pk=self.kwargs['pk'], owner=self.request.user)
        form.instance.patient = patient_profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:show-profile', kwargs={'pk': self.object.patient.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure that patient_profile and its vaccination records are correctly added
        context['patient_profile'] = get_object_or_404(Patient, pk=self.kwargs['pk'], owner=self.request.user)
        context['vaccination_records'] = context['patient_profile'].vaccination_records.all()  # Add vaccination records to the context
        return context



# VaccinationRecord Update View
class VaccinationRecordUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    model = VaccinationRecord
    form_class = VaccinationRecordForm
    template_name = 'profiles/vaccination_record_form.html'

    def get_success_url(self):
        return reverse_lazy('profiles:show-profile', kwargs={'pk': self.object.patientt.pk})


# VaccinationRecord Delete View
class VaccinationRecordDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    model = VaccinationRecord
    template_name = 'profiles/vaccination_record_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('users:show-profile', kwargs={'pk': self.object.patient.pk})
# views.py




class PrescriptionUploadView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('media')
        
        if not files:
            return JsonResponse({'error': 'No files uploaded.'}, status=400)
        
        for file in files:
            upload_type = 'prescription'  # Adjust based on your logic for upload_type
            if file.content_type.startswith('image'):
                media_upload = MediaUpload(user=request.user, upload_type=upload_type, image=file)
            elif file.content_type.startswith('video'):
                media_upload = MediaUpload(user=request.user, upload_type=upload_type, video=file)
            else:
                continue  # Skip unsupported file types
            
            media_upload.save()
        
        return redirect(reverse('profiles:prescription_media_list'))







class PersonalUploadView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('media')
        
        if not files:
            return JsonResponse({'error': 'No files uploaded.'}, status=400)
        
        for file in files:
            upload_type = 'personal'  # Adjust based on your logic for upload_type
            if file.content_type.startswith('image'):
                media_upload = MediaUpload(user=request.user, upload_type=upload_type, image=file)
            elif file.content_type.startswith('video'):
                media_upload = MediaUpload(user=request.user, upload_type=upload_type, video=file)
            else:
                continue  # Skip unsupported file types
            
            media_upload.save()
        
        return redirect(reverse('profiles:personal_media_list'))



@method_decorator(csrf_exempt, name='dispatch')
class MediaDeleteView(LoginRequiredMixin, View):  # Add this view for media deletion
    login_url = 'users:login'

    def delete(self, request, *args, **kwargs):
        media_id = kwargs.get('media_id')
        try:
            media = MediaUpload.objects.get(pk=media_id, user=request.user)
            media.delete()
            return JsonResponse({'message': 'Media deleted successfully.'}, status=200)
        except MediaUpload.DoesNotExist:
            return JsonResponse({'error': 'Media not found.'}, status=404)



class PrescriptionDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    model = MediaUpload
    template_name = 'profiles/media_confirm_delete.html'
    success_url = reverse_lazy('profiles:prescription_media_list') 

class PersonalDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    model = MediaUpload
    template_name = 'profiles/media_confirm_delete.html'
    success_url = reverse_lazy('profiles:personal_media_list') 



class PersonalMediaListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    model = MediaUpload
    template_name = 'profiles/personal_media_list.html'
    context_object_name = 'media_list'

    def get_queryset(self):
        return MediaUpload.objects.filter(user=self.request.user, upload_type='personal')

class PrescriptionMediaListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    model = MediaUpload
    template_name = 'profiles/prescription_media_list.html'
    context_object_name = 'media_list'

    def get_queryset(self):
        return MediaUpload.objects.filter(user=self.request.user, upload_type='prescription')


class PatientListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    model = Patient
    template_name = 'profiles/patient_list.html'
    context_object_name = 'patient'

    def get_queryset(self):
        # Return all PetProfile objects
        return Patient.objects.all()