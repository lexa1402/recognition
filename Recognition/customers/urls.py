from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from customers.views import CustomerList, CustomerDetail, PassportList, PassportDetail, PageScanList, PageScanDetail,\
    PassportScanList, PassportScanDetail, UserList, UserDetail

urlpatterns = [

    path('customer/', CustomerList.as_view()),
    path('customer/<int:pk>/', CustomerDetail.as_view()),

    path('passport/', PassportList.as_view()),
    path('passport/<int:pk>/', PassportDetail.as_view()),

    path('pagescan/', PageScanList.as_view()),
    path('pagescan/<int:pk>/', PageScanDetail.as_view()),

    path('passport_scan', PassportScanList.as_view()),
    path('passport_scan/<int:pk>/', PassportScanDetail.as_view()),

    path('user/', UserList.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),

    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
