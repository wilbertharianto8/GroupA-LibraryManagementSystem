from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from books.models import Book
from .models import BookManagement
from .forms import CombinedBookForm, BookManagementForm, BookForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from books.models import Book
from collections import defaultdict

class BookListView(ListView):
# class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book_management/book_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        return Book.objects.filter(management__isnull=False).order_by('id')



@login_required
def add_book(request):
    if request.method == 'POST':
        form = CombinedBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_management:book_list')
    else:
        form = CombinedBookForm()
    
    return render(request, 'book_management/book_form.html', {
        'form': form,
        'title': 'Add Book'
    })

@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    management = get_object_or_404(BookManagement, book=book)
    
    if request.method == 'POST':
        book_form = BookForm(request.POST, instance=book)
        management_form = BookManagementForm(request.POST, request.FILES, instance=management)
        
        if book_form.is_valid() and management_form.is_valid():
            book = book_form.save()
            management = management_form.save(commit=False)
            management.book = book
            management.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_management:book_list')
    else:
        book_form = BookForm(instance=book)
        management_form = BookManagementForm(instance=management)
    
    return render(request, 'book_management/book_form.html', {
        'book_form': book_form,
        'management_form': management_form,
        'title': 'Edit Book'
    })

class BookDeleteView(DeleteView):
# class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'book_management/book_confirm_delete.html'
    success_url = reverse_lazy('book_management:book_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Book deleted successfully!')
        return response


