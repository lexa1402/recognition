from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from customers.views import CustomerList, CustomerDetail, PassportList, PassportDetail, PageScanList, PageScanDetail, \
    PassportScanList, PassportScanDetail, UserList, UserDetail, api_root

urlpatterns = [
    path('', api_root),

    path('customer/', CustomerList.as_view(), name='customer-list'),
    path('customer/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),

    path('passport/', PassportList.as_view(), name='passport-list'),
    path('passport/<int:pk>/', PassportDetail.as_view(), name='passport-detail'),

    path('pagescan/', PageScanList.as_view(), name='pagescan-list'),
    path('pagescan/<int:pk>/', PageScanDetail.as_view(), name='pagescan-detail'),

    path('passport_scan', PassportScanList.as_view(), name='passportscan-list'),
    path('passport_scan/<int:pk>/', PassportScanDetail.as_view(), name='passportscan-detail'),

    path('user/', UserList.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
