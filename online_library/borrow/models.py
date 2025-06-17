from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from django.utils.timezone import now

# Create your models here.

class BorrowRecord(models.Model):
    BOOK_TYPE_CHOICES = (
        ('physical', 'Physical'),
        ('electronic', 'Electronic'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('return_requested', 'Return Requested'),
        ('return_rejected', 'Return Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_type = models.CharField(max_length=10, choices=BOOK_TYPE_CHOICES)
    borrowed_at = models.DateField()
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)
    request_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    return_rejection_reason = models.TextField(blank=True, null=True)

    def is_overdue(self):
        return self.due_date < now().date() and self.status == 'approved'

    def __str__(self):
        return f"{self.book.title} ({self.get_book_type_display()}) - {self.request_id}"