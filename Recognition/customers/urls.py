from django.urls import path

from customers.views import catalog, customer_list, customer_create, customer_detail, customer_delete, \
    passport_list, passport_create, passport_detail, passport_delete, pagescan_list, pagescan_create, \
    pagescan_detail, pagescan_delete

app_name = 'customers'

urlpatterns = [
    path('', catalog, name='catalog'),

    path('customers/',                  customer_list,      name='customer_list'),
    path('customers/create/',           customer_create,    name='customer_create'),
    path('customer/<int:pk>/',          customer_detail,    name='customer_detail'),
    path('customer/delete/<int:pk>/',   customer_delete,    name='customer_delete'),
    path('customer/delete/',            customer_delete,    name='customer_delete'),

    path('passports/',                  passport_list,      name='passport_list'),
    path('passport/create/',            passport_create,    name='passport_create'),
    path('passport/<int:pk>/',          passport_detail,    name='passport_detail'),
    path('passport/delete/<int:pk>/',   passport_delete,    name='passport_delete'),
    path('passport/delete/',            passport_delete,    name='passport_delete'),

    path('pagescans/',                  pagescan_list,      name='pagescan_list'),
    path('pagescans/create/',           pagescan_create,    name='pagescan_create'),
    path('pagescans/<int:pk>/',         pagescan_detail,    name='pagescan_detail'),
    path('pagescans/delete/<int:pk>/',  pagescan_delete,    name='pagescan_delete'),
    path('pagescan/delete/',            pagescan_delete,    name='pagescan_delete'),
]
