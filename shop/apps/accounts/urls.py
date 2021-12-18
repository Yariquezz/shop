from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login_form, name='login'),
    path('register/', views.register_form, name='register'),
    path('logout/', views.logout_form, name='logout'),
    path('activate/<uidb64>/(<token>/', views.activate, name='activate')
]
