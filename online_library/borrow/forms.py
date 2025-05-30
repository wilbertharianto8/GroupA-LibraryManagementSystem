from django import forms

BORROW_DURATION_CHOICES = [
    (7, '1 week'),
    (14, '2 week'),
    (21, '3 week'),
    (30, '1 month'),
]

class PhysicalBorrowForm(forms.Form):
    duration = forms.ChoiceField(choices=BORROW_DURATION_CHOICES, label="Borrow Duration")