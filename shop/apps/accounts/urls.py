from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login_form, name='login'),
    path('register/', views.register_form, name='register'),
    path('logout/', views.logout_form, name='logout'),
    path(
        'activate/(?P<uidb64>[0-9A-Za-z_]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'
    )
]
