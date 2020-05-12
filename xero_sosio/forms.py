from django import forms

Invoice_Types= [
    ('ACCREC', 'ACCREC'),
    ('ACCPAY', 'ACCPAY')
    ]

class SubmitForm(forms.Form):
    Type = forms.CharField(label='Type:', widget=forms.Select(choices=Invoice_Types))
    ContactID = forms.CharField()
    Date = forms.DateField()
    DueDate = forms.DateField()
    DateString = forms.DateField()
    DueDateString = forms.DateField()
    LineAmountTypes = forms.CharField()
    Description = forms.CharField()
    Quantity = forms.IntegerField()
    UnitAmount = forms.FloatField()
    AccountCode = forms.IntegerField()
    DiscountRate = forms.IntegerField()