from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models
from .forms import SearchForm

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'hospital/dashboard.html')


class PatientListView(ListView):
    model = models.Patient
    paginate_by = 50
    form_class = SearchForm

    def get_queryset(self, **kwargs):
        form = self.form_class(self.request.GET)
        patients = super(PatientListView, self).get_queryset(**kwargs)

        if form.is_valid():
            patients = self.model.objects.filter(name__contains=form.cleaned_data['name'])
            
        return patients

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        context['searchForm'] = SearchForm()
        return context


class PatientDetailView(DetailView):
    model = models.Patient