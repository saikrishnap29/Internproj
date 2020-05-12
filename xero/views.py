from django.shortcuts import render,redirect
from .forms import SubmitForm
import json
# Create your views here.
def home(request):
    form = SubmitForm()
    if request.method == "POST":
        form = SubmitForm(request.POST)
        # form.
        if form.is_valid():
            jsonData = convertFormToJSON(form)
            print(jsonData)

    context = {'form': form, }
    return render(request, 'xero/home.html', context)


def convertFormToJSON(form):
    Type = form.cleaned_data.get('Type')
    Contact = form.cleaned_data.get('ContactID')
    Date = form.cleaned_data.get('Date')
    DueDate = form.cleaned_data.get('DueDate')
    DateString = form.cleaned_data.get('DateString')
    DueDateString = form.cleaned_data.get('DueDateString')
    LineAmountTypes = form.cleaned_data.get('LineAmountTypes')
    Description = form.cleaned_data.get('Description')
    Quantity = form.cleaned_data.get('Quantity')
    UnitAmount = form.cleaned_data.get('UnitAmount')
    AccountCode = form.cleaned_data.get('AccountCode')
    DiscountRate = form.cleaned_data.get('DiscountRate')

    formAsJSON = {
        "Type": Type,
        "Contact": {
            "ContactID": Contact
        },
        "Date": Date,
        "DueDate": DueDate,
        "DateString": DateString,
        "DueDateString": DueDateString,
        "LineAmountTypes": LineAmountTypes,
        "LineItems": [
            {
                "Description": Description,
                "Quantity": str(Quantity),
                "UnitAmount": str(UnitAmount),
                "AccountCode": str(AccountCode),
                "DiscountRate": str(DiscountRate)
            }
        ]
    }

    return json.dumps(formAsJSON, default=str, indent=2);