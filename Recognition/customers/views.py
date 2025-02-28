from django.core.paginator import Paginator
from django.db.models.functions import datetime
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from customers.models import Customer, Passport, PageScan
from customers.recognition import get_passport_data, get_text_data
from customers.forms import PageScanForm, PassportForm, CustomerForm, CustomerListForm, PassportListForm, \
    PageScanListForm


def catalog(request):
    context = {'title': 'Root Page'}
    return render(request, 'customers/catalog.html', context)


# ==================================================== #
# ==================== Page Scans ==================== #
# ==================================================== #


def pagescan_list(request):

    page = int(request.GET.get('page', 1))
    paginator = Paginator(PageScan.objects.all().order_by('-id'), 6)
    current_page = paginator.page(page)

    context = {'pagescan_list': current_page,
               'title': 'Page Scans',
               'form': PageScanListForm()}

    return render(request, 'customers/pagescan-list.html', context)


def pagescan_create(request):

    if request.method == 'GET':
        context = {'form': PageScanForm,
                   'title': 'Page Scan: Create', }
        return render(request, 'customers/pagescan-create.html', context)

    elif request.method == 'POST':
        form = PageScanForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.files.getlist('image')[0]
            mrz_text = None
            mrz_data = get_passport_data(image.file.name)
            if mrz_data['status'] == 'SUCCESS':
                mrz_text = mrz_data['mrz_text']
            PageScan.objects.create(image=image, mrz_text=mrz_text, created=datetime.datetime.now())
            return HttpResponseRedirect(reverse_lazy('customers:pagescan_list'))
        return HttpResponseRedirect(reverse_lazy('customers:pagescan_list'))


def pagescan_detail(request, pk):
    pagescan = PageScan.objects.get(pk=pk)
    context = {'form': PageScanForm,
               'pagescan': pagescan,
               'title': f'Page Scan: {pagescan}'}
    return render(request, 'customers/pagescan-detail.html', context)


class PageScanDelete(DeleteView):
    model = PageScan
    template_name = 'customers/pagescan-confirm-delete.html'
    success_url = reverse_lazy('customers:pagescan_list')


def pagescan_list_delete(request):

    ids = (int(item) for item in request.GET.getlist('is_checked'))

    if request.method == 'GET':
        context = {'object_list': PageScan.objects.filter(pk__in=ids),
                   'title': 'Page Scans: Delete'}
        return render(request, 'customers/pagescan-confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            PageScan.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse_lazy('customers:pagescan_list'))


# =================================================== #
# ==================== Passports ==================== #
# =================================================== #


def passport_list(request):

    page = int(request.GET.get('page', 1))
    paginator = Paginator(Passport.objects.all().order_by('-id'), 12)
    current_page = paginator.page(page)

    context = {'passport_list': current_page,
               'title': 'Passports',
               'form': PassportListForm()}

    return render(request, 'customers/passport-list.html', context)


def passport_create(request):

    if request.method == 'GET':

        from customers.models import state_code

        context = {'form': PassportForm,
                   'state_code': state_code,
                   'title': 'Passport: Create'}
        return render(request, 'customers/passport-detail.html', context)

    elif request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            image = PageScan.objects.get(pk=form.data['page_scan'])
            if image.mrz_text is not None:
                mrz_data = get_text_data(image.mrz_text.replace('\\n', '\n'))
                fields = ('issuer_code', 'surname', 'given_name', 'document_number', 'nationality_code', 'birth_date',
                          'sex', 'expiry_date', 'optional_data_1', 'optional_data_2', )
                data = dict()
                for key in mrz_data.keys():
                    if key in fields:
                        data[key] = mrz_data[key]
                passport = Passport.objects.create(**data, created=datetime.datetime.now())
                passport.page_scan.add(image)
                return HttpResponseRedirect(reverse_lazy('customers:passport_list'))
        return HttpResponseRedirect(reverse_lazy('customers:passport_list'))


def passport_detail(request, pk):

    if request.method == 'GET':

        from customers.models import state_code

        passport = Passport.objects.get(pk=pk)
        context = {'passport': passport,
                   'form': PassportForm(instance=passport),
                   'issuer_code': state_code[passport.issuer_code],
                   'nationality_code': state_code[passport.nationality_code],
                   'title': f'Passport: {passport}'}
        return render(request, 'customers/passport-detail.html', context)

    elif request.method == 'POST':
        form = PassportForm(request.POST, instance=Passport.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('customers:passport_list'))
        return HttpResponseRedirect(reverse_lazy('customers:passport_list'))


class PassportDelete(DeleteView):
    model = Passport
    template_name = 'customers/passport-confirm-delete.html'
    success_url = reverse_lazy('customers:passport_list')


def passport_list_delete(request):

    ids = (int(item) for item in request.GET.getlist('is_checked'))

    if request.method == 'GET':
        context = {'object_list': Passport.objects.filter(pk__in=ids),
                   'title': 'Passports: Delete'}
        return render(request, 'customers/passport-confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            Passport.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse_lazy('customers:passport_list'))


# =================================================== #
# ==================== Customers ==================== #
# =================================================== #


def customer_list(request):

    page = int(request.GET.get('page', 1))
    paginator = Paginator(Customer.objects.all().order_by('-id'), 12)
    current_page = paginator.page(page)

    context = {'customer_list': current_page,
               'title': 'Customers',
               'form': CustomerListForm()}

    return render(request, 'customers/customer-list.html', context)


def customer_create(request):

    if request.method == 'GET':
        context = {'form': CustomerForm,
                   'title': 'Customer: Create', }
        return render(request, 'customers/customer-detail.html', context)

    elif request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            Customer.objects.create(passport=Passport.objects.get(pk=form.data['passport']),
                                    address=form.data['address'],
                                    phone_number=form.data['phone_number'],
                                    email=form.data['email'],
                                    created=datetime.datetime.now())
            return HttpResponseRedirect(reverse_lazy('customers:customer_list'))
        return HttpResponseRedirect(reverse_lazy('customers:customer_list'))


def customer_detail(request, pk):

    if request.method == 'GET':
        customer = Customer.objects.get(pk=pk)
        context = {'customer': customer,
                   'form': CustomerForm(instance=customer),
                   'title': f'Customer: {customer}'}
        return render(request, 'customers/customer-detail.html', context)

    elif request.method == 'POST':
        form = CustomerForm(request.POST, instance=Customer.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('customers:customer_list'))
        return HttpResponseRedirect(reverse_lazy('customers:customer_list'))


class CustomerDelete(DeleteView):
    model = Customer
    template_name = 'customers/customer-confirm-delete.html'
    success_url = reverse_lazy('customers:customer_list')


def customer_list_delete(request):

    ids = (int(item) for item in request.GET.getlist('is_checked'))

    if request.method == 'GET':
        context = {'object_list': Customer.objects.filter(pk__in=ids),
                   'title': 'Customers: Delete'}
        return render(request, 'customers/customer-confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            Customer.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse_lazy('customers:customer_list'))
