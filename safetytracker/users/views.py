from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import StyledUserCreationForm, StyledAuthenticationForm

def register(request):
    """
    Handle new user registration.

    If the request is POST, the submitted UserCreationForm is validated and a new
    user is created. Upon successful registration, the user is automatically logged in
    and redirected to the appropriate page based on their role.
    """
    if request.method == "POST":
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Redirect based on role
            if user.profile.is_manager():
                return redirect("incident:manager-dashboard")
            else:
                return redirect("incident:new-incident")
    else:
        form = StyledUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.

    If the request is POST, the submitted AuthenticationForm is validated. On successful
    authentication, the user is logged in and redirected based on their role.
    """
    if request.method == 'POST':
        form = StyledAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check if there's a 'next' parameter
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            
            # Redirect based on role
            if user.profile.is_manager():
                return redirect('incident:manager-dashboard')
            else:
                return redirect('incident:new-incident')
    else:
        form = StyledAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    Log out the currently authenticated user.

    Only responds to POST requests. After logging out, the user is redirected to login.
    """
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')