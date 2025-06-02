from django.urls import path
from . import views

app_name = 'borrow_history'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]