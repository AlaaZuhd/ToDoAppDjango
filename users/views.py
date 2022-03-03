# users/views.py

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView
from users.forms import CustomUserCreationForm


def dashboard(request):
    return render(request, "users/dashboard.html")


class RegisterView(CreateView):
    model = User
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = "/dashboard/"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.backend = "django.contrib.auth.backends.ModelBackend"
        user.save()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)