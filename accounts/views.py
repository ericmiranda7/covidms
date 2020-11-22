from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.edit import CreateView

from django.contrib.auth import login
# from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class Login(LoginView):
    template_name = 'accounts/login.html'

class Logout(LogoutView):
    template_name = 'accounts/logout.html'