from django.contrib import admin
from . import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Register your models here.
model_list = [
    models.Patient, models.Kin, models.HealthDetails, models.Doctor,
    models.Medicine, models.Ward, models.Bed, models.Ventilator,
    models.LabTest,
]
admin.site.register(model_list)

# Signals to update related models
@receiver(post_save, sender=models.Patient)
def make_bed_unavailable(sender, instance, created, **kwargs):
    bed = instance.bed
    if instance.bed:
        bed.available = False
        bed.save()
