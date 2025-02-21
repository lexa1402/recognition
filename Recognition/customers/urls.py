from django.urls import path, include
from rest_framework import routers

from customers.views import CustomerViewSet, PassportViewSet, PageScanViewSet


router = routers.DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'passport', PassportViewSet)
router.register(r'page_scan', PageScanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
