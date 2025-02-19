# from django.shortcuts import render

from rest_framework import permissions, viewsets, generics
# from rest_framework import mixins, response
# from django.http import HttpResponse, JsonResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView

from customers.models import Customer, Passport, PassportScan, PageScan
from customers.serializers import CustomerSerializer, PassportSerializer, PassportScanSerializer, PageScanSerializer


# ==================== Customers ====================


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# ==================== Passports ====================


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer
    permission_classes = [permissions.IsAdminUser]


class PassportList(generics.ListCreateAPIView):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer


class PassportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer


# ==================== PageScans ====================


class PageScanViewSet(viewsets.ModelViewSet):
    queryset = PageScan.objects.all()
    serializer_class = PageScanSerializer
    permission_classes = [permissions.IsAdminUser]


class PageScanList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = PageScanSerializer


class PageScanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = PageScanSerializer


# ==================== PassportScans ====================


class PassportScanViewSet(viewsets.ModelViewSet):
    queryset = PassportScan.objects.all()
    serializer_class = PassportScanSerializer
    permission_classes = [permissions.IsAdminUser]


class PassportScanList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = PassportScanSerializer


class PassportScanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = PassportScanSerializer


# ==================== What happens in APIViews without mixins ====================
#
#
# class CustomerList(APIView):
#
#     def get(self, request, format=None):
#         customers = Customer.objects.all()
#         serializer = CustomerSerializer(customers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, format=None):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CustomerDetail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Customer.objects.get(pk=pk)
#         except Customer.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, pk, format=None):
#         customer = self.get_object(pk)
#         serializer = CustomerSerializer(customer)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         customer = self.get_object(pk)
#         serializer = CustomerSerializer(customer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         customer = self.get_object(pk)
#         customer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# ==================== How to use mixins in APIViews ====================
#
#
# class CustomerList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def set(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class CustomerDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
#                      mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def update(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
