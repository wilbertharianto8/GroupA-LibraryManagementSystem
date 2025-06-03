from django.urls import path
from . import views

app_name = 'borrow_history'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download/<int:record_id>/', views.download_digital_book, name='download_digital_book'),
]