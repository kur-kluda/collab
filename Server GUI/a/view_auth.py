from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse

class Login(LoginView):
    template_name = "auth_login.html"

class UserRegistration(CreateView):
    template_name = "auth_user_registration.html"
    form_class = UserCreationForm

    def get_success_url(self):
        for i in self.request.GET:
            #print(self.request.GET[i])
            if i=="next":
                return self.request.GET[i]
        return reverse("login")