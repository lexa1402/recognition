from cv2 import imread, convertScaleAbs
from django.core.paginator import Paginator
from django.db.models.functions import datetime
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from customers.forms import PageScanForm, PassportForm, CustomerForm, CustomerListForm, PassportListForm, \
    PageScanListForm
from customers.models import Customer, Passport, PageScan, get_free_passports, get_free_pagescans
from customers.recognition import get_text_data, get_mrz


def catalog(request):
    context = {'title': 'Root Page', }
    return render(request, 'customers/catalog.html', context)


# ==================================================== #
# ==================== Page Scans ==================== #
# ==================================================== #


def pagescan_list(request):
    page = int(request.GET.get('page', 1))
    paginator = Paginator(PageScan.objects.all().order_by('-id'), 20)
    current_page = paginator.page(page)

    context = {'pagescan_list': current_page,
               'title': 'Page Scans',
               'form': PageScanListForm(), }

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
            for file in files:
                mrz_text = get_mrz(convertScaleAbs(imread(file.file.name), alpha=0.18))
                pagescan = PageScan.objects.create(image=file, mrz_text=mrz_text, created=datetime.datetime.now())
            if files.__len__() == 1:
                messages.success(request, 'Page scan uploaded.')
                return HttpResponseRedirect(reverse('customers:pagescan_detail', kwargs={'pk': pagescan.id}))
            messages.success(request, f'Page scans ({files.__len__()}) uploaded')
        return HttpResponseRedirect(reverse('customers:pagescan_list'))


def pagescan_detail(request, pk):
    pagescan = PageScan.objects.get(pk=pk)
    context = {'pagescan': pagescan,
               'title': f'Page Scan: {pagescan}', }
    return render(request, 'customers/pagescan-detail.html', context)


def pagescan_delete(request, pk=None):
    ids = [pk] if pk else [int(item) for item in request.GET.getlist('is_checked')]

    if request.method == 'GET':
        context = {'object_list': PageScan.objects.filter(pk__in=ids),
                   'title': 'Page Scans: Delete',
                   'pagescan': True, }
        return render(request, 'customers/confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            PageScan.objects.get(pk=pk).delete()
        messages.info(request, f'Page scans ({ids.__len__()}) deleted.')
        return HttpResponseRedirect(reverse('customers:pagescan_list'))


# =================================================== #
# ==================== Passports ==================== #
# =================================================== #


def passport_list(request):
    page = int(request.GET.get('page', 1))
    paginator = Paginator(Passport.objects.all().order_by('-id'), 20)
    current_page = paginator.page(page)

    context = {'passport_list': current_page,
               'pagescan_list': PageScan.objects.all(),
               'title': 'Passports',
               'form': PassportListForm(),
               'register': get_free_pagescans().__len__() > 0, }

    return render(request, 'customers/passport-list.html', context)


def passport_create(request):

    if request.method == 'GET':
        from customers.models import state_code
        context = {'form': PassportForm,
                   'state_code': state_code,
                   'title': 'Passport: Create', }
        return render(request, 'customers/passport-detail.html', context)

    elif request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            pagescan = PageScan.objects.get(pk=form.data['page_scan'])
            mrz_data = get_text_data(pagescan.mrz_text.replace('\\n', '\n'))
            passport = Passport.objects.create(
                **{key: mrz_data[key] for key in filter(lambda key: key in Passport.fields(), mrz_data)},
                created=datetime.datetime.now(), )
            passport.page_scan.add(pagescan)
            messages.success(request, f'Passport ({passport}) created.')
            return HttpResponseRedirect(reverse('customers:passport_detail', kwargs={'pk': passport.id}))
        return HttpResponseRedirect(reverse('customers:passport_list'))


def passport_detail(request, pk):

    if request.method == 'GET':
        from customers.models import state_code
        passport = Passport.objects.get(pk=pk)
        context = {'passport': passport,
                   'form': PassportForm(instance=passport),
                   'issuer': state_code[passport.issuer_code],
                   'nationality': state_code[passport.nationality_code],
                   'title': f'Passport: {passport}', }
        return render(request, 'customers/passport-detail.html', context)

    elif request.method == 'POST':
        form = PassportForm(request.POST, instance=Passport.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.info(request, f'Passport ({form.instance}) changes saved.')
        return HttpResponseRedirect(reverse('customers:passport_list'))


def passport_delete(request, pk=None):
    ids = (pk, ) if pk else [int(item) for item in request.GET.getlist('is_checked')]

    if request.method == 'GET':
        context = {'object_list': Passport.objects.filter(pk__in=ids),
                   'title': 'Passports: Delete',
                   'passport': True, }
        return render(request, 'customers/confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            Passport.objects.get(pk=pk).delete()
        messages.info(request, f'Passport(s) ({ids.__len__()}) deleted.')
        return HttpResponseRedirect(reverse('customers:passport_list'))


def passport_upload(request):
    free_scans = get_free_pagescans()
    for pagescan in free_scans:
        mrz_data = get_text_data(pagescan.mrz_text.replace('\\n', '\n'))
        passport = Passport.objects.create(
            **{key: mrz_data[key] for key in filter(lambda key: key in Passport.fields(), mrz_data.keys())},
            created=datetime.datetime.now(), )
        passport.page_scan.add(pagescan)
    messages.success(request, f'Passports ({free_scans.__len__()}) created.')
    return HttpResponseRedirect(reverse('customers:passport_list'))


# =================================================== #
# ==================== Customers ==================== #
# =================================================== #


def customer_list(request):
    page = int(request.GET.get('page', 1))
    paginator = Paginator(Customer.objects.all().order_by('-id'), 20)
    current_page = paginator.page(page)

    context = {'customer_list': current_page,
               'title': 'Customers',
               'form': CustomerListForm(),
               'register': get_free_passports().__len__() > 0, }

    return render(request, 'customers/customer-list.html', context)


def customer_create(request):

    if request.method == 'GET':
        context = {'form': CustomerForm,
                   'title': 'Customer: Create', }
        return render(request, 'customers/customer-detail.html', context)

    elif request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.create(
                **{key: form.data[key] for key in Customer.fields()},
                passport=Passport.objects.get(pk=form.data['passport']),
                created=datetime.datetime.now(), )
            messages.success(request, f'Customer ({customer}) created')
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
            messages.info(request, f'Customer ({form.instance}) changes saved')
            return HttpResponseRedirect(reverse('customers:customer_list'))
        return HttpResponseRedirect(reverse('customers:customer_list'))


def customer_delete(request, pk=None):
    ids = (pk, ) if pk else [int(item) for item in request.GET.getlist('is_checked')]

    if request.method == 'GET':
        context = {'object_list': Customer.objects.filter(pk__in=ids),
                   'title': 'Customers: Delete',
                   'customer': True}
        return render(request, 'customers/confirm-delete.html', context)

    elif request.method == 'POST':
        for pk in ids:
            Customer.objects.get(pk=pk).delete()
        messages.info(request, f'Customers ({ids.__len__()}) deleted.')
        return HttpResponseRedirect(reverse('customers:customer_list'))


def customer_upload(request):
    free_passports = get_free_passports()
    for passport in free_passports:
        Customer.objects.create(passport=passport, created=datetime.datetime.now())
    messages.info(request, f'Customers ({free_passports.__len__()}) created.')
    return HttpResponseRedirect(reverse('customers:customer_list'))
