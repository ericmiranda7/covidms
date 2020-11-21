from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models
from .forms import SearchForm

import matplotlib.pyplot as plt
import io
import urllib, base64

# Create your views here.


@login_required
def dashboard(request):
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

    context = {}
    context['statistics'] = statistics

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


def graph(request):
    plt.plot(range(10))
    fig = plt.gcf()
    buf = io.ByteIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string= base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request,dashboard.html,{'data':uri})