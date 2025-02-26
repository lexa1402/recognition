from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from customers.models import Customer, Passport, PageScan
from customers.serializers import CustomerSerializer, PassportSerializer, PageScanSerializer
from customers.recognition import get_passport_data, get_text_data
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


class PageScanList(ListView):
    model = PageScan
    template_name = 'customers/pagescan-list.html'


def pagescan_create(request):

    if request.method == 'GET':
        context = {'form': PageScanForm, }
        return render(request, 'customers/pagescan-create.html', context)

    elif request.method == 'POST':
        form = PageScanForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.files.getlist('image')[0]
            mrz_text = None
            mrz_data = get_passport_data(image.file.name)
            if mrz_data['status'] == 'SUCCESS':
                mrz_text = mrz_data['mrz_text']
            PageScan.objects.create(image=image, mrz_text=mrz_text)
            return HttpResponseRedirect(reverse_lazy('customers:pagescan_list'))
        return HttpResponseRedirect(reverse_lazy('customers:pagescan_list'))


def pagescan_detail(request, pk):

    if request.method == 'GET':
        context = {'form': PageScanForm,
                   'pagescan': PageScan.objects.get(pk=pk), }
        return render(request, 'customers/pagescan-detail.html', context)


class PageScanDelete(DeleteView):
    model = PageScan
    template_name = 'customers/pagescan-confirm-delete.html'
    success_url = reverse_lazy('customers:pagescan_list')
