from django.http import Http404, FileResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from borrow.models import BorrowRecord
from book_management.models import BookManagement
from django.utils.timezone import now

# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    active_tab = request.GET.get('tab', 'physical')
    current_filter = request.GET.get('status', 'all')

    physical_filter_options = ['all', 'pending', 'approved', 'rejected', 'returned', 'overdue']
    digital_filter_options = ['all', 'approved', 'overdue']

    physical_records = BorrowRecord.objects.filter(user=user, book_type='physical').order_by('-borrowed_at')
    digital_records = BorrowRecord.objects.filter(user=user, book_type='electronic').order_by('-borrowed_at')

    def filter_records(records, status_filter):
        if status_filter == 'all':
            return records
        elif status_filter == 'overdue':
            return records.filter(
                status='approved',
                due_date__lt=now().date(),
                returned_at__isnull=True
            )
        elif status_filter == 'approved':
            return records.filter(
                status='approved',
                returned_at__isnull=True,
                due_date__gte=now().date()
            )
        else:
            return records.filter(status=status_filter)

    physical_filtered = filter_records(physical_records, current_filter if active_tab == 'physical' else 'all')
    digital_filtered = filter_records(digital_records, current_filter if active_tab == 'digital' else 'all')

    def group_by_status(records):
        grouped = {}
        today = now().date()

        for record in records:
            if record.status == 'approved' and record.due_date and record.due_date < today and not record.returned_at:
                key = 'overdue'
            else:
                key = record.status
            grouped.setdefault(key, []).append(record)
        return grouped

    physical_history = group_by_status(physical_filtered)
    digital_history = group_by_status(digital_filtered)

    context = {
        'active_tab': active_tab,
        'current_filter': current_filter,
        'physical_filter_options': physical_filter_options,
        'digital_filter_options': digital_filter_options,
        'physical_history': physical_history,
        'digital_history': digital_history,
    }

    return render(request, 'history/dashboard.html', context)

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
