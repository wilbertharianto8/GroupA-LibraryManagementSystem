from django import forms
from books.models import Book
from books.forms import BookForm
from .models import BookManagement

class BookManagementForm(forms.ModelForm):
    class Meta:
        model = BookManagement
        fields = ['book_type', 'file', 'location_code']
        widgets = {
            'book_type': forms.RadioSelect(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book_type'].widget.attrs.update({'class': 'form-check-input'})
        
    def clean(self):
        cleaned_data = super().clean()
        book_type = cleaned_data.get('book_type')
        file = cleaned_data.get('file')
        location_code = cleaned_data.get('location_code')
        
        if book_type == 'electronic' and not file:
            self.add_error('file', 'Please upload a file for electronic books.')
        elif book_type == 'physical' and not location_code:
            self.add_error('location_code', 'Please provide a location code for physical books.')
            
        return cleaned_data

class CombinedBookForm:
    def __init__(self, *args, **kwargs):
        self.book_form = BookForm(*args, **kwargs)
        self.management_form = BookManagementForm(*args, **kwargs)
        
    def is_valid(self):
        return self.book_form.is_valid() and self.management_form.is_valid()
        
    def save(self):
        book = self.book_form.save()
        # Get or create the management record
        management, created = BookManagement.objects.get_or_create(
            book=book,
            defaults={
                'book_type': self.management_form.cleaned_data['book_type'],
                'file': self.management_form.cleaned_data.get('file'),
                'location_code': self.management_form.cleaned_data.get('location_code')
            }
        )
        # If the record already existed, update it
        if not created:
            management.book_type = self.management_form.cleaned_data['book_type']
            if 'file' in self.management_form.cleaned_data:
                management.file = self.management_form.cleaned_data['file']
            if 'location_code' in self.management_form.cleaned_data:
                management.location_code = self.management_form.cleaned_data['location_code']
            management.save()
        return book