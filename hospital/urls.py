from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.PatientListView.as_view(), name='patients'),
    path('patient/<int:pk>', views.PatientDetailView.as_view(), name='detail'),
]