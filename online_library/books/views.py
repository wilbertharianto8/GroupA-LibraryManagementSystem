from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Book, Genre
from .forms import BookForm, GenreForm
# from borrowing.models import Borrowing
from django.http import JsonResponse
from django.views.decorators.http import require_POST

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.all()
        search_query = self.request.GET.get('search', '')
        genre_filter = self.request.GET.get('genre', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(isbn__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if genre_filter:
            queryset = queryset.filter(genres__id=genre_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['genre_filter'] = self.request.GET.get('genre', '')
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        #     context['user_borrowings'] = Borrowing.objects.filter(
        #         user=self.request.user, 
        #         book=self.object
        #     ).order_by('-request_date')
        return context

class BookCreateView(UserPassesTestMixin, CreateView):
# class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')
    
    def test_func(self):
        return self.request.user.is_administrator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Book added successfully!')
        return super().form_valid(form)

class BookUpdateView(UserPassesTestMixin, UpdateView):
# class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')
    
    def test_func(self):
        return self.request.user.is_administrator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)

class BookDeleteView(UserPassesTestMixin, DeleteView):
# class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:book_list')
    
    def test_func(self):
        return self.request.user.is_administrator()
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Genre management views
class GenreListView(UserPassesTestMixin, ListView):
# class GenreListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Genre
    template_name = 'books/genre_list.html'
    context_object_name = 'genres'
    
    def test_func(self):
        return self.request.user.is_administrator()

class GenreCreateView(UserPassesTestMixin, CreateView):
# class GenreCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'books/genre_form.html'
    success_url = reverse_lazy('books:genre_list')
    
    def test_func(self):
        return self.request.user.is_administrator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Genre added successfully!')
        return super().form_valid(form)

class GenreUpdateView(UserPassesTestMixin, UpdateView):
# class GenreUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'books/genre_form.html'
    success_url = reverse_lazy('books:genre_list')
    
    def test_func(self):
        return self.request.user.is_administrator()
    
    def form_valid(self, form):
        messages.success(self.request, 'Genre updated successfully!')
        return super().form_valid(form)

class GenreDeleteView(UserPassesTestMixin, DeleteView):
# class GenreDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Genre
    template_name = 'books/genre_confirm_delete.html'
    success_url = reverse_lazy('books:genre_list')
    
    def test_func(self):
        return self.request.user.is_administrator()
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Genre deleted successfully!')
        return super().delete(request, *args, **kwargs)

# @login_required
@require_POST
def add_genre_ajax(request):
    name = request.POST.get('name')
    description = request.POST.get('description', '')
    
    if not name:
        return JsonResponse({'success': False, 'error': 'Genre name is required'})
    
    try:
        genre = Genre.objects.create(name=name, description=description)
        return JsonResponse({
            'success': True,
            'genre': {
                'id': genre.id,
                'name': genre.name
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


