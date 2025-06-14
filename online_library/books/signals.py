from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models import Book
from book_management.models import BookManagement

@receiver(post_save, sender=Book)
def create_book_management(sender, instance, created, **kwargs):
    if created:
        BookManagement.objects.get_or_create(book=instance)