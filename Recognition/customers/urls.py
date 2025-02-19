from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from customers.views import CustomerViewSet, PassportViewSet, PageScanViewSet, PassportScanViewSet, UserViewSet


# ==================== Manual Routing Setup ====================


# customer_list = CustomerViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })
#
# customer_detail = CustomerViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy',
# })


router = routers.DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'passport', PassportViewSet)
router.register(r'page_scan', PageScanViewSet)
router.register(r'passport_scan', PassportScanViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # path('customer/', customer_list, name='customer-list'),
    # path('customer/<int:pk>/', customer_detail.as_view(), name='customer-detail'),
    #
    # path('passport/', PassportList.as_view(), name='passport-list'),
    # path('passport/<int:pk>/', PassportDetail.as_view(), name='passport-detail'),
    #
    # path('pagescan/', PageScanList.as_view(), name='pagescan-list'),
    # path('pagescan/<int:pk>/', PageScanDetail.as_view(), name='pagescan-detail'),
    #
    # path('passport_scan', PassportScanList.as_view(), name='passportscan-list'),
    # path('passport_scan/<int:pk>/', PassportScanDetail.as_view(), name='passportscan-detail'),
    #
    # path('user/', UserList.as_view(), name='user-list'),
    # path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    #
    # path('api-auth/', include('rest_framework.urls')),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
