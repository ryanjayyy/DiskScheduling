from django.urls import path
from diskscheduling import views


urlpatterns = [
    path('', views.home, name='home'),

]