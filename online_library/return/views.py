from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from borrow.models import BorrowRecord
from books.models import Book
from datetime import timedelta

# Create your views here.

LATE_FEE_PER_DAY = 1.00

def return_book(request, record_id):
    borrow = get_object_or_404(BorrowRecord, id=record_id)

    if request.method == 'POST':
        today = now().date()
        borrow.returned_at = today

        borrow.status = 'returned'

        if today > borrow.due_date:
            days_late = (today - borrow.due_date).days
            late_fee = days_late * LATE_FEE_PER_DAY
        else:
            late_fee = 0.0

        if borrow.book_type == 'physical':
            try:
                book = borrow.book
                book.available_copies = min(book.available_copies + 1, book.total_copies)
                book.save()
            except (Book.DoesNotExist, ValueError):
                print(f"[ERROR] Could not find book with ID {borrow.book} to update stock.")

        borrow.save()

        return render(request, 'return/return_success.html', {
            'borrow': borrow,
            'late_fee': late_fee,
        })
    return render(request, 'return/return_confirm.html', {
        'borrow': borrow,
    })