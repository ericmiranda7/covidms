from django.contrib import admin
from . import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

# Register your models here.
model_list = [
    models.Kin, models.Doctor,
    models.Medicine, models.Ward, models.Bed, models.Ventilator,
    models.LabTest,
]
admin.site.register(model_list)


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity', 'admit_date', 'get_ward']
    list_filter = ['severity']
    search_fields = ['name', 'aadhar', 'insurance', 'status',]

    def get_ward(self, obj):
        try:
            return obj.bed.ward
        except:
            return 'Not assigned bed'
    get_ward.admin_order_field = 'bed__ward'
    get_ward.short_description = 'Ward No.'


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

