from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from customers.models import Customer, Passport, PageScan
from customers.serializers import CustomerSerializer, PassportSerializer, PageScanSerializer
from customers.recognition import get_passport_data
from customers.forms import PageScanForm


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
                    if 'optional_data' in passport_data.keys():
                        serializer.validated_data['optional_data_1'] = passport_data['optional_data']

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


def catalog(request):

    url_name = request.resolver_match.url_name
    context = {
        'page': url_name,
    }

    if url_name == 'customers':
        context['customers'] = Customer.objects.all()
    elif url_name == 'passports':
        context['passports'] = Passport.objects.all()
    elif url_name == 'pagescans':
        context['pagescans'] = PageScan.objects.all()

    return render(request, 'customers/catalog.html', context=context)


def customer(request, pk=None):

    if request.method == 'GET':
        context = {'passports': Passport.objects.all(),
                   'fill': False, }
        if pk:
            context['customer'] = Customer.objects.get(pk=pk)
            context['fill'] = True

    return render(request, 'customers/customer.html', context)


def passport(request, pk=None):

    from customers.models import state_code

    if request.method == 'GET':
        context = {'passport': Passport.objects.get(pk=pk),
                   'state_code': state_code,
                   'fill': True, }

    elif request.method == 'POST':
        context = {'state_code': state_code,
                   'fill': False, }

    return render(request, 'customers/passport.html', context=context)


def pagescan(request, pk=None):

    if request.method == 'GET':
        context = {'form': PageScanForm(),
                   'fill': False}
        if pk:
            context['pagescan'] = PageScan.objects.get(pk=pk)
            context['fill'] = True
        return render(request, 'customers/pagescan.html', context)

    elif request.method == 'POST':
        form = PageScanForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/success/")
        return HttpResponseRedirect("/bad_request/")
