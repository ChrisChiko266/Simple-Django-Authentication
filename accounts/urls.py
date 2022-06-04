from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password-reset-sent.html'), name='password-reset-done'
    ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password-reset-confirm.html'), {
    },
        name='password-reset-confirm'
    ),
    path('password-reset/', views.PasswordResetRequest.as_view(), name='password-reset'),
]
