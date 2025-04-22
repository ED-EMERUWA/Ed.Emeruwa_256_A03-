from django.shortcuts import redirect

def custom_404(request, exception=None):
    # Redirect to a specific page, e.g., home or a custom page
    return redirect('user_login')  # Replace 'home' with the URL name of the page you want to redirect to
