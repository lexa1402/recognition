from django.urls import path, include
from rest_framework import routers

from customers.views import CustomerViewSet, PassportViewSet, PageScanViewSet, catalog, passport, pagescan, customer

app_name = 'customers'

# router = routers.DefaultRouter()
# router.register(r'customer', CustomerViewSet)
# router.register(r'passport', PassportViewSet)
# router.register(r'page_scan', PageScanViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('',                    catalog,    name='catalog'),
    path('customers/',          catalog,    name='customers'),
    path('customers/create/',   customer,   name='customer_create'),
    path('customers/<int:pk>/', customer,   name='customer_get'),
    path('passports/',          catalog,    name='passports'),
    path('passports/create/',   passport,   name='passport_create'),
    path('passports/<int:pk>/', passport,   name='passports_get'),
    path('pagescans/',          catalog,    name='pagescans'),
    path('pagescans/create/',   pagescan,   name='pagescan_create'),
    path('pagescans/<int:pk>/', pagescan,   name='pagescan_get'),
]
