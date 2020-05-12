from django.urls import path
from.import views
urlpatterns=[
    path('XeroFirstAuth/',views.XeroFirstAuth,name='XeroFirstAuth'),
    path('',views.process_callback_view,name='process_callback_view'),
    path('',views.calls_xero,name='calls_xero'),
    path('XeroTenants/',views.XeroTenants,name='XeroTenants'),
    path('',views.XeroRefreshToken,name='XeroRefreshToken'),
    path('',views.XeroRequests,name='XeroRequests'),
    path('export_csv/',views.export_json,name='export_json'),
    path('home/',views.home,name='home'),
]