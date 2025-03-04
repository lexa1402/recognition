from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db.models.functions import datetime
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from customers.models import Customer, Passport, PageScan
from customers.recognition import get_passport_data, get_text_data
from customers.forms import PageScanForm, PassportForm, CustomerForm, CustomerListForm, PassportListForm, \
    PageScanListForm


def catalog(request):
    context = {'title': 'Root Page'}
    return render(request, 'customers/catalog.html', context)


def get_free_pagescans():
    pagescans = PageScan.objects.annotate(counter=Count('passport'))
    pagescans = pagescans.filter(counter=0)
    pagescans = pagescans.filter(~Q(mrz_text=None))
    return pagescans


def get_free_passports():
    passports = Passport.objects.annotate(counter=Count('customer'))
    passports = passports.filter(counter=0)
    return passports


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
        return render(request, 'customers/pagescan-detail.html', context)

    elif request.method == 'POST':
        form = PageScanForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.files.getlist('image')
            for image in files:
                mrz_text = None
                mrz_data = get_passport_data(image.file.name)
                if mrz_data['status'] == 'SUCCESS':
                    mrz_text = mrz_data['mrz_text']
                pagescan = PageScan.objects.create(image=image, mrz_text=mrz_text, created=datetime.datetime.now())
            if files.__len__() == 1:
                return HttpResponseRedirect(reverse('customers:pagescan_detail', kwargs={'pk': pagescan.id}))
        return HttpResponseRedirect(reverse('customers:pagescan_list'))


def pagescan_detail(request, pk):
    pagescan = PageScan.objects.get(pk=pk)
    context = {'pagescan': pagescan,
               'title': f'Page Scan: {pagescan}'}
    return render(request, 'customers/pagescan-detail.html', context)


def pagescan_delete(request, pk=None):

    if pk:
        ids = [pk]
    else:
        ids = (int(item) for item in request.GET.getlist('is_checked'))

    if request.method == 'GET':
        context = {'object_list': PageScan.objects.filter(pk__in=ids),
                   'title': 'Page Scans: Delete',
                   'pagescan': True, }
        return render(request, 'customers/confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            PageScan.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('customers:pagescan_list'))


# =================================================== #
# ==================== Passports ==================== #
# =================================================== #


def passport_list(request):

    page = int(request.GET.get('page', 1))
    paginator = Paginator(Passport.objects.all().order_by('-id'), 12)
    current_page = paginator.page(page)

    context = {'passport_list': current_page,
               'pagescan_list': PageScan.objects.all(),
               'title': 'Passports',
               'form': PassportListForm(),
               'register': False, }

    if get_free_pagescans().__len__() > 0:
        context['register'] = True

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
            pagescan = PageScan.objects.get(pk=form.data['page_scan'])
            mrz_data = get_text_data(pagescan.mrz_text.replace('\\n', '\n'))
            fields = ('issuer_code', 'surname', 'given_name', 'document_number', 'nationality_code', 'birth_date',
                      'sex', 'expiry_date', 'optional_data_1', 'optional_data_2', )
            data = dict()
            for key in mrz_data.keys():
                if key in fields:
                    data[key] = mrz_data[key]
            passport = Passport.objects.create(**data, created=datetime.datetime.now())
            passport.page_scan.add(pagescan)
            return HttpResponseRedirect(reverse('customers:passport_detail', kwargs={'pk': passport.id}))
        return HttpResponseRedirect(reverse('customers:passport_list'))


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
            return HttpResponseRedirect(reverse('customers:passport_list'))
        return HttpResponseRedirect(reverse('customers:passport_list'))


def passport_delete(request, pk=None):

    if pk:
        ids = [pk]
    else:
        ids = (int(item) for item in request.GET.getlist('is_checked'))

    if request.method == 'GET':
        context = {'object_list': Passport.objects.filter(pk__in=ids),
                   'title': 'Passports: Delete',
                   'passport': True, }
        return render(request, 'customers/confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            Passport.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('customers:passport_list'))


def passport_upload(request):
    for pagescan in get_free_pagescans():
        mrz_data = get_text_data(pagescan.mrz_text.replace('\\n', '\n'))
        fields = ('issuer_code', 'surname', 'given_name', 'document_number', 'nationality_code', 'birth_date',
                  'sex', 'expiry_date', 'optional_data_1', 'optional_data_2',)
        data = dict()
        for key in mrz_data.keys():
            if key in fields:
                data[key] = mrz_data[key]
        passport = Passport.objects.create(**data, created=datetime.datetime.now())
        passport.page_scan.add(pagescan)
    return HttpResponseRedirect(reverse('customers:passport_list'))


# =================================================== #
# ==================== Customers ==================== #
# =================================================== #


def customer_list(request):

    page = int(request.GET.get('page', 1))
    paginator = Paginator(Customer.objects.all().order_by('-id'), 12)
    current_page = paginator.page(page)

    context = {'customer_list': current_page,
               'title': 'Customers',
               'form': CustomerListForm(),
               'register': False, }

    if get_free_passports().__len__() > 0:
        context['register'] = True

    return render(request, 'customers/customer-list.html', context)


def customer_create(request):

    if request.method == 'GET':
        context = {'form': CustomerForm,
                   'title': 'Customer: Create', }
        return render(request, 'customers/customer-detail.html', context)

    elif request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.create(passport=Passport.objects.get(pk=form.data['passport']),
                                               address=form.data['address'],
                                               phone_number=form.data['phone_number'],
                                               email=form.data['email'],
                                               created=datetime.datetime.now())
            return HttpResponseRedirect(reverse('customers:customer_detail', kwargs={'pk': customer.id}))
        return HttpResponseRedirect(reverse('customers:customer_list'))


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
            return HttpResponseRedirect(reverse('customers:customer_list'))
        return HttpResponseRedirect(reverse('customers:customer_list'))


def customer_delete(request, pk=None):

    if pk:
        ids = [pk]
    else:
        ids = (int(item) for item in request.GET.getlist('is_checked'))

    if request.method == 'GET':
        context = {'object_list': Customer.objects.filter(pk__in=ids),
                   'title': 'Customers: Delete',
                   'customer': True}
        return render(request, 'customers/confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            Customer.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('customers:customer_list'))


def customer_upload(request):
    for passport in get_free_passports():
        Customer.objects.create(passport=passport, created=datetime.datetime.now())
    return HttpResponseRedirect(reverse('customers:customer_list'))
