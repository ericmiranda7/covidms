from django.contrib import admin
from . import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Register your models here.
model_list = [
    models.Kin, models.Doctor,
    models.Medicine, models.Ward, models.Bed, models.Ventilator,
    models.LabTest,
]
admin.site.register(model_list)


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity']
    list_filter = ['severity']
    search_fields = ['name', 'aadhar']

    """ def get_severity(self, obj):
        return obj.health_details.severity
    get_severity.admin_order_field = 'health_details__severity'
    get_severity.short_description = 'Severity' """

    # Filtering on side


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

@receiver(post_save, sender=models.HealthDetails)
def derive_severity(sender, instance, created, **kwargs):
    try:
        patient = instance.patient
        print('hi')
        print(instance.calculate_severity())
        patient.severity = instance.calculate_severity()
        patient.save()
    except:
        pass

