from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from borrow.models import BorrowRecord
from books.models import Book
from datetime import timedelta
from django.contrib import messages

# Create your views here.

LATE_FEE_PER_DAY = 1.00

def return_book(request, record_id):
    borrow_record = get_object_or_404(BorrowRecord, id=record_id, user=request.user)

    if borrow_record.book_type != 'physical' or \
       borrow_record.status not in ['approved', 'overdue', 'return_rejected']:
        messages.error(request, "This book cannot be returned at this time or is not a physical book.")
        return redirect('borrow_history:dashboard')

    if request.method == 'POST':
        borrow_record.status = 'return_requested'
        borrow_record.save()
        messages.success(request, f"Return request for '{borrow_record.book.title}' has been submitted for librarian review.")
        return redirect('borrow_history:dashboard')

    return render(request, 'return/return_confirm.html', {
        'borrow': borrow_record,
    })