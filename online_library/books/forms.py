from django import forms
from .models import Book, Genre

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'isbn', 'description', 'genres', 'publication_year', 
                 'publisher', 'cover_image', 'total_copies', 'available_copies')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'genres':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['genres'].widget.attrs.update({'class': 'form-select'})
        self.fields['description'].widget.attrs.update({'rows': 4})

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name', 'description')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': 3}) 