import uuid
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from books.models import Book
from .models import BorrowRecord
from .forms import PhysicalBorrowForm
from django.http import FileResponse, Http404
from book_management.models import BookManagement
from datetime import datetime

# Create your views here.

# @login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'borrow/book_detail.html', {
        'book': book,
        'has_physical': book.total_copies > 0,
        'has_digital': book.hasattr(book, 'digitalbook')
    })

# @login_required
def borrow_physical(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.available_copies <= 0:
        messages.error(request, 'No physical copies available for borrowing.')
        return redirect('borrow:book_detail', book_id=book.id)

    if request.method == 'POST':
        form = PhysicalBorrowForm(request.POST)
        if form.is_valid():
            duration_days = int(form.cleaned_data['duration'])
            due_date = now().date() + timedelta(days=duration_days)

            borrow_record = BorrowRecord.objects.create(
                user=request.user,
                book=book,
                book_type='physical',
                borrowed_at=now().date(),
                due_date=due_date,
                request_id=uuid.uuid4().hex[:10].upper(),
                status='pending'
            )

            messages.success(request, f'Request submitted. ID: {borrow_record.request_id}')
            return redirect('borrow:borrow_detail', record_id=borrow_record.id)

    else:
        form = PhysicalBorrowForm()

    return render(request, 'borrow/borrow_physical.html', {
        'book': book,
        'form': form
    })

# @login_required
def borrow_digital(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    borrow_record = BorrowRecord.objects.create(
        user=request.user,
        book=book,
        book_type='electronic',
        borrowed_at=now().date(),
        due_date=now().date() + timedelta(days=15),
        request_id=uuid.uuid4().hex[:10].upper(),
        status='approved'
    )

    messages.success(request, f'Digital book borrowed successfully. ID: {borrow_record.request_id}')
    return redirect('borrow:borrow_detail', record_id=borrow_record.id)

# @login_required
def borrow_detail(request, record_id):
    borrow = get_object_or_404(BorrowRecord, id=record_id, user=request.user)
    return render(request, 'borrow/borrow_detail.html', {'borrow': borrow, 'now': now()})

# @login_required
def download_digital_book(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id, user=request.user)

    if record.book_type != 'electronic' or record.status != 'approved':
        raise Http404("You do not have permission to download this book.")

    try:
        management = BookManagement.objects.get(book=record.book, book_type='electronic')
    except BookManagement.DoesNotExist:
        raise Http404("Digital version not available.")

    if not management.file:
        raise Http404("Digital file is missing.")

    return FileResponse(management.file.open('rb'), as_attachment=True, filename=management.file.name)
