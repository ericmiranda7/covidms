from django.db import models
from datetime import date

# Create your models here.
from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_status = [
        (1, 'Admitted'),
        (2, 'Discharged'),
        (3, 'Recovered'),
        (4, 'Deceased'),
    ]

    name = models.CharField(max_length=32)
    dob = models.DateField()
    address = models.CharField(max_length=128)
    phone_no = models.IntegerField()
    next_of_kin = models.ForeignKey('Kin', on_delete=models.CASCADE, blank=True, null=True)
    insurance = models.CharField(max_length=16)
    aadhar = models.IntegerField()
    status = models.IntegerField(choices=patient_status, default=1)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, blank=True, null=True)
    admit_date = models.DateTimeField()
    discharge_date = models.DateTimeField(blank=True, null=True)
    bed = models.OneToOneField('Bed', on_delete=models.SET_NULL, blank=True, null=True)
    medicines = models.ManyToManyField('Medicine', blank=True)
    health_details = models.OneToOneField('HealthDetails', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    def age(self):
        years = date.today() - self.dob
        return int(years.days / 365)


class Kin(models.Model):
    name = models.CharField(max_length=32)
    phone_no = models.IntegerField()

    def __str__(self):
        return self.name

class HealthDetails(models.Model):
    diseases = [
        ('DB', 'Diabeties'),
        ('CD', 'Cardiovascular Disease'),
    ]
    severities = [
        (1, 'Mild'),
        (2, 'Potenitally worsening'),
        (3, 'Moderate severity'),
        (4, 'High severity'),
        (5, 'Requires urgent care'),
    ]

    #symptoms
    fever = models.BooleanField(default=False)
    dry_cough = models.BooleanField(default=False)
    tiredness = models.BooleanField(default=False)

    # less common symptoms
    aches = models.BooleanField(default=False)
    sore_throat = models.BooleanField(default=False)
    diarrhoea = models.BooleanField(default=False)
    conjunctivitis = models.BooleanField(default=False)
    headache = models.BooleanField(default=False)
    loss_of_taste_or_smell = models.BooleanField(default=False)
    rash = models.BooleanField(default=False)

    #serious symptoms
    shortness_of_breath = models.BooleanField(default=False)
    chest_pain = models.BooleanField(default=False)
    loss_of_speech = models.BooleanField(default=False)
    

    severity = models.IntegerField(choices=severities, default=1)
    comorbid = models.CharField(
        max_length=12,
        choices=diseases,
        blank=True,
        null=True,
    )
    blood_group = models.CharField(max_length=3, default='UNK')
    is_smoker = models.BooleanField(default=False)
    is_drinker = models.BooleanField(default=False)

    def __str__(self):
        return self.patient.name + "'s Health Record"


class Doctor(models.Model):
    name = models.CharField(max_length=32)
    phone_no = models.IntegerField()

    def __str__(self):
        return self.name


class Medicine(models.Model):
    category_types = [
        ('PK', 'Painkiller'),
        ('BT', 'Blood thinner'),
        ('LX', 'Laxative'),
        ('AI', 'Anti inflammatory')
    ]
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=2, choices=category_types)
    expiry = models.DateField()
    qty = models.IntegerField()
    threshold_value = models.IntegerField()

    def __str__(self):
        return self.name


class Ward(models.Model):
    type_list = [
        ('ICU', 'ICU'),
        ('GEN', 'General'),
    ]

    type = models.CharField(max_length=3, choices=type_list)

    def __str__(self):
        return self.type + ' ' + str(self.id)

class Bed(models.Model):
    available = models.BooleanField(default=True)
    ward = models.ForeignKey('Ward', on_delete=models.CASCADE)
    ventilator = models.ManyToManyField('Ventilator', blank=True)

    def __str__(self):
        return 'Bed ' + str(self.id)

class Ventilator(models.Model):
    available = models.BooleanField(default=True)

    def __str__(self):
        return 'Ventilator ' + str(self.id)

class LabTest(models.Model):
    type_choices = [
        ('AG', 'Antigen'),
        ('RT', 'RT-PCR'),
    ]

    result_choices = [
        ('P', 'Positive'),
        ('N', 'Negative'),
    ]

    type = models.CharField(max_length=2, choices=type_choices)
    result = models.CharField(max_length=1, choices=result_choices)
    testing_date = models.DateTimeField()
    test_duration = models.IntegerField('Hours until test results')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Lab test ' + str(self.id)
