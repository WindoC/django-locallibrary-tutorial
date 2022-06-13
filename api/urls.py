from django.urls import path

from . import views

urlpatterns = [
    path('get-msisdn/<str:ip>', views.get_msisdn, name='get-msisdn'),
    path('get-ip/<str:msisdn>', views.get_ip, name='get-ip'),
]

urlpatterns += [
    path('healthcheck/', views.healthcheck, name='healthcheck'),
]