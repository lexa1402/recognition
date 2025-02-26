from django.urls import path, include
from rest_framework import routers

from customers.views import catalog
from customers.views import PassportList, PageScanList, PageScanDelete, PassportDelete
from customers.views import passport_create, pagescan_create, pagescan_detail, passport_detail
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

    path('passports/',                  PassportList.as_view(),     name='passport_list'),
    path('passport/create/',            passport_create,            name='passport_create'),
    path('passport/<int:pk>/',          passport_detail,            name='passport_detail'),
    path('passport/delete/<int:pk>/',   PassportDelete.as_view(),   name='passport_delete'),

    path('pagescans/',                  PageScanList.as_view(),     name='pagescan_list'),
    path('pagescans/create/',           pagescan_create,            name='pagescan_create'),
    path('pagescans/<int:pk>/',         pagescan_detail,            name='pagescan_detail'),
    path('pagescans/delete/<int:pk>/',  PageScanDelete.as_view(),   name='pagescan_delete'),
]
