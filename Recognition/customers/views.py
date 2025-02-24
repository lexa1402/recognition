from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from customers.models import Customer, Passport, PageScan
from customers.serializers import CustomerSerializer, PassportSerializer, PageScanSerializer
from customers.recognition import get_passport_data


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):

        context = {'request': request}
        serializer = PassportSerializer(data=request.data, context=context)

        if serializer.is_valid():
            valid_data = False

            for pagescan in serializer.validated_data['page_scan']:
                passport_path = f'images/{pagescan.image.name}'
                passport_data = get_passport_data(passport_path)
                if passport_data['status'] == 'SUCCESS':
                    valid_data = True
                    for key in passport_data.keys():
                        if key in request.data.keys():
                            serializer.validated_data[key] = passport_data[key]

            if not valid_data:
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

            temp = serializer.validated_data['page_scan']
            serializer.validated_data.pop('page_scan')

            passport = Passport.objects.create(**serializer.validated_data)
            for pagescan in temp:
                passport.page_scan.add(pagescan)

            return Response(PassportSerializer(passport, context=context).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageScanViewSet(viewsets.ModelViewSet):
    queryset = PageScan.objects.all()
    serializer_class = PageScanSerializer
    permission_classes = [permissions.IsAdminUser]
