from django.urls import path
from .views import return_book

app_name = 'return'

urlpatterns = [
    path('<int:record_id>/', return_book, name='return'),
]