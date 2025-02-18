from django.shortcuts import render
from rest_framework import permissions, viewsets

from customers.models import Customer, Passport, PassportScan, PageScan
from customers.serializers import CustomerSerializer, PassportSerializer, PassportScanSerializer, PageScanSerializer

# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all().order_by('id')
    serializer_class = PassportSerializer
    permission_classes = [permissions.IsAdminUser]


class PageScanViewSet(viewsets.ModelViewSet):
    queryset = PageScan.objects.all().order_by('id')
    serializer_class = PageScanSerializer
    permission_classes = [permissions.IsAdminUser]


class PassportScanViewSet(viewsets.ModelViewSet):
    queryset = PassportScan.objects.all().order_by('passport')
    serializer_class = PassportScanSerializer
    permission_classes = [permissions.IsAdminUser]
