from django.urls import path
from . import views

app_name = 'borrow'

urlpatterns = [
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('physical/<int:book_id>/', views.borrow_physical, name='borrow_physical'),
    path('digital/<int:book_id>/', views.borrow_digital, name='borrow_digital'),
    path('detail/<int:record_id>/', views.borrow_digital, name='borrow_detail'),
    path('download/<int:record_id>/', views.download_digital_book, name='download_digital_book'),
]