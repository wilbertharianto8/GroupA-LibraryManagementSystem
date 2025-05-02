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
        management = self.management_form.save(commit=False)
        management.book = book
        management.save()
        return book 