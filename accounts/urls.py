from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
	path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    # path('', views.index)
]