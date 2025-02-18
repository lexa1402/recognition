from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from customers.models import Customer, Passport, PassportScan, PageScan
from customers.serializers import CustomerSerializer, PassportSerializer, PassportScanSerializer, PageScanSerializer

# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['GET', 'POST'])
def customer_list(request):

    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk):

    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all().order_by('id')
    serializer_class = PassportSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['GET', 'POST'])
def passport_list(request):

    if request.method == 'GET':
        passports = Passport.objects.all()
        serializer = PassportSerializer(passports, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PassportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def passport_detail(request, pk):

    try:
        passport = Passport.objects.get(pk=pk)
    except Passport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PassportSerializer(passport)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PassportSerializer(passport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        passport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PageScanViewSet(viewsets.ModelViewSet):
    queryset = PageScan.objects.all().order_by('id')
    serializer_class = PageScanSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['GET', 'POST'])
def page_scan_list(request):

    if request.method == 'GET':
        page_scans = PageScan.objects.all()
        serializer = PageScanSerializer(page_scans, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PageScanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def page_scan_detail(request, pk):

    try:
        page_scan = PageScan.objects.get(pk=pk)
    except PageScan.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PageScanSerializer(page_scan)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PageScanSerializer(page_scan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        page_scan.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class PassportScanViewSet(viewsets.ModelViewSet):
    queryset = PassportScan.objects.all().order_by('passport')
    serializer_class = PassportScanSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['GET', 'POST'])
def passport_scan_list(request):

    if request.method == 'GET':
        passport_scans = PassportScan.objects.all()
        serializer = PassportScanSerializer(passport_scans, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PassportScanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def passport_scan_detail(request, pk):

    try:
        passport_scan = PassportScan.objects.get(pk=pk)
    except PassportScan.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PassportScanSerializer(passport_scan)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PassportScanSerializer(passport_scan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        passport_scan.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
