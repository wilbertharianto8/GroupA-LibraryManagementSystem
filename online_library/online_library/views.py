from django.http import JsonResponse
from django.shortcuts import render
from books.models import Book
from django.db.models import Q

def home(request):
    # Get featured books (you can modify this query based on your criteria)
    featured_books = Book.objects.filter(is_featured=True)[:6]
    
    context = {
        'featured_books': featured_books,
        'search_query': request.GET.get('search', '')
    }
    return render(request, 'home.html', context) 

# @login_required
def search_books(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query)
        ).values('id', 'title', 'author', 'description')
        return JsonResponse(list(books), safe=False)
    return JsonResponse([], safe=False)