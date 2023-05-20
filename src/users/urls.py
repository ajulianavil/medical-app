from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("registro", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('registro2', views.contact, name='registro2'),
    path('profile', views.profile, name='profile'),
    path('user_data', views.user_data, name='user_data'),    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="users/password/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/password/password_reset sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="users/password/password_reset_done.html"), name="password_reset_complete")
]