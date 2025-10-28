from django.contrib.auth.decorators import user_passes_test

def manager_required(function=None, redirect_url='/'):
    """
    Decorator for views that checks if the user is a manager.
    Redirects to the specified URL if the user is not a manager.
    """
    def check_manager(user):
        if not user.is_authenticated:
            return False
        return hasattr(user, 'profile') and user.profile.is_manager()
    
    actual_decorator = user_passes_test(check_manager, login_url=redirect_url)

    if function:
        return actual_decorator(function)
    return actual_decorator


def employee_or_manager_required(function=None, redirect_url='/users/login/'):
    """
    Decorator for views that checks if the user is logged in.
    Just an alias for login_required, but keeping naming consistent.
    """
    from django.contrib.auth.decorators import login_required
    actual_decorator = login_required(login_url=redirect_url)

    if function:
        return actual_decorator(function)
    return actual_decorator