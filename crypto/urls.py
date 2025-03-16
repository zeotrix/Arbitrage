from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('update-brokers-data/', views.update_brokers_data, name='update_brokers_data'),

]