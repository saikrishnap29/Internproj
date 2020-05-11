from django import forms
class SubmitForm(forms.Form):
    Type = forms.CharField()
    Contact = forms.CharField()
    Date = forms.DateField()
    DueDate = forms.DateField()
    LineAmountTypes = forms.CharField()
    Description = forms.CharField()
    Quantity = forms.IntegerField()
    UnitAmount = forms.FloatField()
    AccountCode = forms.IntegerField()
    DiscountRate = forms.IntegerField()