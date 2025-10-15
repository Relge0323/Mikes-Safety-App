from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import StyledUserCreationForm, StyledAuthenticationForm

def register(request):
    """
    Handle new user registration.

    If the request is POST, the submitted UserCreationForm is validated and a new
    user is created. Upon successful registration, the user is automatically logged in
    and redirected to the incident list. For GET requests, an empty registration form
    is displayed.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'users/register.html' template with the registration form,
                      or a redirect to the incident list after successful registration.
    """
    if request.method == "POST":
        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("incident:list")
    else:
        form = StyledUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.

    If the request is POST, the submitted AuthenticationForm is validated. On successful
    authentication, the user is logged in and redirected to the page specified in 'next'
    (if provided) or to the incident list. For GET requests, an empty login form is displayed.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'users/login.html' template with the login form,
                      or a redirect after successful login.
    """
    if request.method == 'POST':
        form = StyledAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('incident:list')
    else:
        form = StyledAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    Log out the currently authenticated user.

    Only responds to POST requests. After logging out, the user is redirected to the
    incident list page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirect to the incident list after logout.
    """
    if request.method == 'POST':
        logout(request)
        return redirect('incident:list')