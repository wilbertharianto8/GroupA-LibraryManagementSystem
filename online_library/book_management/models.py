from django.db import models
from books.models import Book
from django.core.validators import FileExtensionValidator

class BookManagement(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='management')
    book_type = models.CharField(max_length=10, choices=[
        ('physical', 'Physical Book'),
        ('electronic', 'Electronic Book'),
    ], default='physical')
    location_code = models.CharField(max_length=20, blank=True, null=True)  # For physical books
    file = models.FileField(
        upload_to='books/electronic/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'epub', 'mobi'])]
    )  # For electronic books
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} - {self.book_type}"

    def save(self, *args, **kwargs):
        # if self.book_type == 'physical' and not self.location_code:
        #     # Generate a random location code for physical books
        #     import random
        #     import string
        #     self.location_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

