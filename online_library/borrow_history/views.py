from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from borrow.models import BorrowRecord
from django.utils.timezone import now

# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    records = BorrowRecord.objects.filter(user=user).order_by('-borrowed_at')

    history = []
    for record in records:
        if record.returned_at:
            status = 'Returned'
        elif record.due_date < now().date():
            status = 'Overdue'
        else:
            status = 'Active'
        history.append({'record': record, 'status': status})

    return render(request, 'history/dashboard.html', {'history': history})