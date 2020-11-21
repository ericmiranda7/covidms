from django.contrib import admin
from . import models

# Register your models here.
models = [
    models.Patient, models.Kin, models.HealthDetails, models.Doctor,
    models.Medicine, models.Ward, models.Bed, models.Ventilator,
    models.LabTest,
]
admin.site.register(models)
