from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.login_view, name='home'),                # This is the login page
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('forgot-password/', views.forgot_password_request, name='forgot_password_request'),
    path('reset-password/', views.forgot_password_verify, name='forgot_password_verify'),
    path('change_password/', views.change_password, name='change_password'),
]
