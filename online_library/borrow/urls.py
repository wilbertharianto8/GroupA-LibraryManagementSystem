from django.urls import path
from . import views

app_name = 'borrow'

urlpatterns = [
    path('options/<int:book_id>/', views.book_detail, name='book_detail'),
    path('physical/<int:book_id>/', views.borrow_physical, name='borrow_physical'),
    path('digital/<int:book_id>/', views.borrow_digital, name='borrow_digital'),
    path('detail/<int:record_id>/', views.borrow_detail, name='borrow_detail'),
]