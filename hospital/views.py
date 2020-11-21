from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import models

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'hospital/dashboard.html')


class PatientListView(ListView):
    model = models.Patient
    paginate_by = 50

class PatientDetailView(DetailView):
    model = models.Patient