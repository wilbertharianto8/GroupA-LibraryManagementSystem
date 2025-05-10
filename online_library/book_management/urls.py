from django.urls import path
from . import views

app_name = 'book_management'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete_book'),
    
] 