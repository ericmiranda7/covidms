from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models
from .forms import SearchForm
from datetime import date

# Create your views here.


@login_required
def dashboard(request):
    # Patient statistics
    patients = models.Patient.objects.all()

    statistics = {
        "recovered": 0,
        "admitted": 0,
        "deceased": 0,
    }

    for patient in patients:
        if patient.status == 1:
            statistics['admitted'] += 1
        elif patient.status == 3:
            statistics['recovered'] += 1
        elif patient.status == 4:
            statistics['deceased'] += 1

        # Severity algorithm
        days_since = date.today() - patient.admit_date.date()
        if (days_since.days > 5):
            patient.severity_score += 9
            patient.severity_score = 23 if patient.severity_score > 23 else patient.severity_score
            patient.severity = (patient.severity_score / 23) * 4
            patient.save()



    # Bed & ventilator statistics
    beds = models.Bed.objects.all()
    ventilators = models.Ventilator.objects.all()
    free_bed_count = 0
    used_ventilator_count = 0
    for bed in beds:
        if bed.available:
            free_bed_count += 1
        if bed.ventilator:
            used_ventilator_count += 1


    # Lab statistics
    labtests = models.LabTest.objects.all()
    lab_pos = 0
    lab_neg = 0

    for test in labtests:
        if test.result == 'P':
            lab_pos += 1
        if test.result == 'N':
            lab_neg += 1


    context = {}
    context['statistics'] = statistics
    context['beds'] = beds
    context['vents'] = ventilators
    context['free_beds'] = free_bed_count
    context['used_vents'] = used_ventilator_count
    context['lab_tests'] = labtests
    context['lab_pos'] = lab_pos
    context['lab_neg'] = lab_neg
    
    return render(request, 'hospital/dashboard.html', context)


class PatientListView(ListView):
    model = models.Patient
    paginate_by = 50
    form_class = SearchForm

    def get_queryset(self, **kwargs):
        form = self.form_class(self.request.GET)
        patients = super(PatientListView, self).get_queryset(**kwargs)

        if form.is_valid():
            patients = self.model.objects.filter(
                name__contains=form.cleaned_data['name'])

            sort = form.cleaned_data['severity']
            if sort == '1':
                print('sort name')
                patients = patients.order_by('name')
            if sort == '2':
                patients = patients.order_by('-health_details__severity')

        return patients

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        context['searchForm'] = SearchForm()
        return context


class PatientDetailView(DetailView):
    model = models.Patient
