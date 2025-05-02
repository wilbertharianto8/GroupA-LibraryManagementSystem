from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # Book URLs
    path('', views.BookListView.as_view(), name='book_list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('add/', views.BookCreateView.as_view(), name='book_add'),
    path('<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    
    # Genre URLs
    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genres/add/', views.GenreCreateView.as_view(), name='genre_add'),
    path('genres/add/ajax/', views.add_genre_ajax, name='genre_add_ajax'),
    path('genres/<int:pk>/edit/', views.GenreUpdateView.as_view(), name='genre_edit'),
    path('genres/<int:pk>/delete/', views.GenreDeleteView.as_view(), name='genre_delete'),
] 