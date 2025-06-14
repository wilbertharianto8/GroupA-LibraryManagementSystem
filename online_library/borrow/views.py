import uuid
from datetime import timedelta

from book_management.models import BookManagement
from books.models import Book
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .forms import PhysicalBorrowForm
from .models import BorrowRecord

# Create your views here.

# @login_required
def borrow_physical(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.available_copies <= 0:
        messages.error(request, 'No physical copies available for borrowing.')
        return render(request,'borrow/borrow_physical.html', {
            'book': book,
            'form': None
        })

    if request.method == 'POST':
        existing = BorrowRecord.objects.filter(
            user=request.user,
            book=book,
            due_date__gte=now().date(),
            status__in=['pending', 'approved'],
        ).exists()

        if existing:
            messages.error(request, 'You have already borrowed this book and the period is still active.')
            return redirect('borrow:borrow_physical', book_id=book.id)

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
            messages.success(request, f'Request submitted to librarian, please wait for approval.')
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

    if request.method == 'POST':
        existing = BorrowRecord.objects.filter(
            user=request.user,
            book=book,
            due_date__gte=now().date(),
            status__in=['approved'],
        ).exists()
        if existing:
            messages.error(request, 'You have already borrowed this book and the borrow period is still active.')
        else:
            BorrowRecord.objects.create(
                user=request.user,
                book=book,
                book_type='electronic',
                borrowed_at=now().date(),
                due_date=now().date() + timedelta(days=15),
                request_id=uuid.uuid4().hex[:10].upper(),
                status='approved'
            )
            messages.success(request, f'Digital book borrowed successfully.')
        return render(request, 'borrow/borrow_digital.html', {'book': book})
    return render(request, 'borrow/borrow_digital.html', {'book': book})

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

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    title = book.title

    physical_book = Book.objects.filter(title=title, management__book_type='physical').first()
    digital_book = Book.objects.filter(title=title, management__book_type='electronic').first()

    physical_mng = BookManagement.objects.filter(book=book, book_type='physical').first()
    digital_mng = BookManagement.objects.filter(book=book, book_type='electronic').first()

    physical_available = physical_mng is not None and book.available_copies > 0
    digital_available = digital_mng is not None and getattr(digital_mng, 'file', None)

    return render(request, 'borrow/book_detail.html', {
        'book': book,
        'physical_book': physical_book,
        'digital_book': digital_book,
    })