from django.urls import path

from customers.views import catalog, customer_detail, customer_create, passport_list, customer_list
from customers.views import passport_create, pagescan_create, pagescan_detail, passport_detail, pagescan_list
from customers.views import PassportList, PageScanList, PageScanDelete, PassportDelete, CustomerList, CustomerDelete

# from django.urls import include
# from customers.views import CustomerViewSet, PassportViewSet, PageScanViewSet
# from rest_framework import routers

app_name = 'customers'

# router = routers.DefaultRouter()
# router.register(r'customer', CustomerViewSet)
# router.register(r'passport', PassportViewSet)
# router.register(r'page_scan', PageScanViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('', catalog, name='catalog'),

    path('customers/',                  customer_list,              name='customer_list'),
    path('customers/create/',           customer_create,            name='customer_create'),
    path('customer/<int:pk>/',          customer_detail,            name='customer_detail'),
    path('customer/delete/<int:pk>/',   CustomerDelete.as_view(),   name='customer_delete'),

    path('passports/',                  passport_list,              name='passport_list'),
    path('passport/create/',            passport_create,            name='passport_create'),
    path('passport/<int:pk>/',          passport_detail,            name='passport_detail'),
    path('passport/delete/<int:pk>/',   PassportDelete.as_view(),   name='passport_delete'),

    path('pagescans/',                  pagescan_list,              name='pagescan_list'),
    path('pagescans/create/',           pagescan_create,            name='pagescan_create'),
    path('pagescans/<int:pk>/',         pagescan_detail,            name='pagescan_detail'),
    path('pagescans/delete/<int:pk>/',  PageScanDelete.as_view(),   name='pagescan_delete'),
]
