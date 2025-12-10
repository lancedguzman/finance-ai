from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def login_view(request):
    """View to login a user."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to dashboard (tracker) after login
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('tracker:index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """View to logout a user."""
    if request.method == 'POST':
        logout(request)
        return redirect('user_management:login')
    
    # Optional: If you want to handle GET logout (less secure but common)
    logout(request) 
    return redirect('user_management:login')


def register(request):
    """View to register a new user."""
    if request.method == 'POST':
        # Use the custom form here
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tracker:index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='user_management:login')
def profile(request):
    """View to display and update user profile."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # We try to get the existing profile, or create one if it doesn't exist
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user_management:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)
