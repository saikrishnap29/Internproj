import os
from django.shortcuts import render,redirect
from .forms import SubmitForm
from xero.auth import PublicCredentials

import json
import requests
import webbrowser
import base64

from django.http import HttpResponseRedirect
from django.core.cache import caches

from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes


def XeroFirstAuth(request):
        credentials = OAuth2Credentials(
        'client_id', 'client_secret', callback_uri='https://xero.com/',
        scope=[XeroScopes.OFFLINE_ACCESS, XeroScopes.ACCOUNTING_CONTACTS,
               XeroScopes.ACCOUNTING_TRANSACTIONS]
    )
        authorization_url = credentials.generate_url()
        caches['mycache'].set('xero_creds', credentials.state)
        return HttpResponseRedirect(authorization_url)

def process_callback_view(request):
    cred_state = caches['mycache'].get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    auth_secret = request.get_raw_uri()
    credentials.verify(auth_secret)
    credentials.set_default_tenant()
    caches['mycache'].set('xero_creds', credentials.state)


def calls_xero(request):
    cred_state = caches['mycache'].get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    if credentials.expired():
        credentials.refresh()
        caches['mycache'].set('xero_creds', credentials.state)
    xero = Xero(credentials)

    contacts = xero.contacts.all()

def XeroTenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                            headers={
                                'Authorization': 'Bearer ' + access_token,
                                'Content-Type': 'application/json'
                            })
    json_response = response.json()
    print(json_response)

    for tenants in json_response:
        json_dict = tenants
    return json_dict['tenantId']


def XeroRefreshToken(refresh_token):
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                             headers={
                                 'Authorization': 'Basic ' + b64_id_secret,
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             },
                             data={
                                 'grant_type': 'refresh_token',
                                 'refresh_token': refresh_token
                             })
    json_response = response.json()
    print(json_response)

    new_refresh_token = json_response['refresh_token']
    rt_file = open('C:/folder/refresh_token.txt', 'w')
    rt_file.write(new_refresh_token)
    rt_file.close()
    return [json_response['access_token'], json_response['refresh_token']]


def XeroRequests():
    old_refresh_token = open('C:/folder/refresh_token.txt', 'r').read()
    new_tokens = XeroRefreshToken(old_refresh_token)
    xero_tenant_id = XeroTenants(new_tokens[0])

    get_url = 'https://api.xero.com/api.xro/2.0/Invoices'
    response = requests.get(get_url,
                            headers={
                                'Authorization': 'Bearer ' + tokens[0],
                                'Xero-tenant-id': xero_tenant_id,
                                'Accept': 'application/json'
                            })
    json_response = response.json()
    print(json_response)

    xero_output = open('C:/folder/xero_output.txt', 'w')
    xero_output.write(response.text)
    xero_output.close()

def export_json():
    invoices = open(r'C:\folder\xero_output.txt', 'r').read()
    json_invoice = json.loads(invoices)
    analysis = open(r'C:\folder\analysis.csv', 'w')
    analysis.write('Type' + ',' + 'Total')
    analysis.write('\n')
    for invoices in json_invoice['Invoices']:
        analysis.write(invoices['Type'] + ',' + str(invoices['Total']))
        analysis.write('\n')
    analysis.close()


def home(request):
    form = SubmitForm()
    if request.method == "POST":
        form = SubmitForm(request.POST)
        # form.
        if form.is_valid():
            jsonData = convertFormToJSON(form)
            print(jsonData)

    context = {'form': form, }
    return render(request, 'xero_sosio/home.html', context)


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

    return json.dumps(formAsJSON, default=str, indent=2)