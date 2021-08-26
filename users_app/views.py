from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .forms import CreateUserForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        register_form= CreateUserForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,("login to get started"))
            return redirect('register')
    else:
        register_form= CreateUserForm()
        return render(request,'register.html',{'register_form':register_form})