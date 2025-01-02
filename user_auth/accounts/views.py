from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
import random
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                validate_email(email) 
            except ValidationError:
                form.add_error('email', 'Enter a valid email address.')
            else:
                if User.objects.filter(email=email).exists():
                    form.add_error('email', 'This email is already registered.')
                elif User.objects.filter(username=form.cleaned_data.get('username')).exists():
                    form.add_error('username', 'This username is already taken.')
                else:
                    user = form.save()  
                    return redirect('home') 
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def show_authentication_error_messages(request, username_or_email, form):
    if User.objects.filter(username=username_or_email).exists():
        # messages.error(request, 'Password is incorrect.')
        form.add_error('password', 'Password is incorrect.')
    elif User.objects.filter(email=username_or_email).exists():
        # messages.error(request, 'Password is incorrect.')
        form.add_error('password', 'Password is incorrect.')
    else:
        if '@' in username_or_email:
            form.add_error('email', 'Please enter correct email address.')
            # messages.error(request, 'Please enter correct email address.')
        else:
            form.add_error('username', 'Please enter correct username.')
            # messages.error(request, 'Please enter correct username.')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username_or_email, password=password) or \
                   authenticate(request, email=username_or_email, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                show_authentication_error_messages(request,username_or_email, form)

        else:
            username_or_email = form.cleaned_data.get('username', '')
            show_authentication_error_messages(request,username_or_email,form)

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


def forgot_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {
                'error': 'No account found with that email address.'
            })

        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_expiry = now() + timedelta(minutes=10)  # OTP valid for 10 minutes
        user.save()

        send_mail(
            'Password Reset Code',
            f'Your password reset code is {otp}. It is valid for 10 minutes.',
            'rajprabhakar1516@gmail.com',
            [email],
        )

        return render(request, 'accounts/forgot_password_verify.html', {
            'message': 'A reset code has been sent to your email.',
            'email': email
        })

    return render(request, 'accounts/forgot_password.html')


def forgot_password_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password_verify.html', {
                'error': 'Invalid email or OTP.',
                'email': email
            })

        if user.otp != otp or now() > user.otp_expiry:
            return render(request, 'accounts/forgot_password_verify.html', {
                'error': 'Invalid or expired OTP.',
                'email': email
            })

        if new_password != confirm_password:
            return render(request, 'accounts/forgot_password_verify.html', {
                'error': 'Passwords do not match.',
                'email': email
            })

        user.password = make_password(new_password)
        user.otp = None  
        user.otp_expiry = None 
        user.save()

        return redirect('/')

    return render(request, 'accounts/forgot_password_verify.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            form.save()
            
            request.user.backend = 'django.contrib.auth.backends.ModelBackend'

            
            login(request, request.user)
            
            return redirect('dashboard')
        else:
            for errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})