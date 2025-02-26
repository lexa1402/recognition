from django.urls import path, include
from rest_framework import routers

from customers.views import *
# from customers.views import CustomerViewSet, PassportViewSet, PageScanViewSet

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
    path('customers/', catalog, name='customers'),

    path('passports/', catalog, name='passports'),

    path('pagescans/',                  PageScanList.as_view(),     name='pagescan_list'),
    path('pagescans/<int:pk>/',         pagescan_detail,            name='pagescan_detail'),
    path('pagescans/create/',           pagescan_create,            name='pagescan_create'),
    path('pagescans/delete/<int:pk>/',  PageScanDelete.as_view(),   name='pagescan_delete'),
]
