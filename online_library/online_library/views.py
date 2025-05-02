from django.shortcuts import render
from books.models import Book

def home(request):
    # Get featured books (you can modify this query based on your criteria)
    featured_books = Book.objects.filter(is_featured=True)[:6]
    
    context = {
        'featured_books': featured_books,
        'search_query': request.GET.get('search', '')
    }
    return render(request, 'home.html', context) 