from django.contrib import admin
from . import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User

from django import template

register = template.Library()


# Register your models here.
model_list = [
    models.Kin,
    models.Medicine, models.Ward, models.Bed, models.Ventilator,
    models.LabTest,
]
admin.site.register(model_list)


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity', 'admit_date', 'get_ward', 'doctor']
    list_filter = ['severity', 'doctor', 'bed__ward']
    search_fields = ['name', 'aadhar', 'insurance', 'status', 'doctor__name']

    def get_ward(self, obj):
        try:
            return obj.bed.ward
        except:
            return 'Not assigned bed'
    get_ward.admin_order_field = 'bed__ward'
    get_ward.short_description = 'Ward No.'

@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'patients']


@admin.register(models.HealthDetails)
class HealthDetailsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('comorbid', 'blood_group', ('is_smoker', 'is_drinker'))
        }),
        ('Symptoms', {
            'fields': (
                ('fever', 'dry_cough', 'tiredness', 'aches', 'sore_throat',
                'diarrhoea', 'conjunctivitis', 'headache', 'rash',
                'loss_of_taste_or_smell', 'shortness_of_breath',
                'chest_pain', 'loss_of_speech'),
            )
        })
    )

# Signals to update related models
@receiver(post_save, sender=models.Patient)
def make_bed_unavailable(sender, instance, created, **kwargs):
    bed=instance.bed
    if instance.bed:
        bed.available=False
        bed.save()

@receiver(pre_delete, sender=models.Patient)
def make_bed_available(sender, instance, **kwargs):
    bed = instance.bed
    if instance.bed:
        bed.available=True
        bed.save()


@receiver(post_save, sender=models.HealthDetails)
def derive_severity(sender, instance, created, **kwargs):
    try:
        patient = instance.patient
        patient.severity = instance.calculate_severity()
        patient.save()
    except:
        pass

@receiver(post_save, sender=User)
def create_doctor(sender, instance, created, **kwargs):
    if created:
        models.Doctor.objects.create(user=instance, name=instance.username)
    instance.doctor.save()

@receiver(post_save, sender=models.Patient)
def assign_doctor(sender, instance, created, **kwargs):
    dr_set = models.Doctor.objects.all()
    for dr in dr_set:
        dr.patients = dr.patient_set.all().count()
        dr.save()

    qs = dr_set.order_by('patients')
    instance.doctor = qs[0]
    if created:
        instance.save()

@receiver(pre_delete, sender=models.Patient)
def free_doctor(sender, instance, **kwargs):
    instance.doctor.patients -= 1
    instance.doctor.save()

