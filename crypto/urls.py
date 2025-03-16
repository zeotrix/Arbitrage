from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('update-nobitex-data/', views.update_nobitex_data, name='update_nobitex_data'),

]