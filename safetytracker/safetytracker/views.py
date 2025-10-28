from django.shortcuts import redirect

def home_view(request):
    """
    Redirect users based on authentication status.
    - Not authenticated: redirect to login
    - Authenticated: redirect to appropriate page based on role
    """
    # If user is not logged in, bring them to login page
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    # If user is a manager, show them the dashboard
    if request.user.profile.is_manager():
        return redirect('incident:manager-dashboard')
    
    # If user is an employee, redirect to report incident page
    return redirect('incident:new-incident')