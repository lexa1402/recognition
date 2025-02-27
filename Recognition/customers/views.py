from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy

from customers.models import Customer, Passport, PageScan
from customers.recognition import get_passport_data, get_text_data
from customers.forms import PageScanForm, PassportForm, CustomerForm
from customers.models import state_code


def catalog(request):
    return render(request, 'customers/catalog.html')


# ====================================================
# ==================== Page Scans ====================
# ====================================================


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


# ===================================================
# ==================== Passports ====================
# ===================================================


class PassportList(ListView):
    model = Passport
    template_name = 'customers/passport-list.html'


def passport_create(request):

    if request.method == 'GET':
        context = {'form': PassportForm,
                   'state_code': state_code, }
        return render(request, 'customers/passport-detail.html', context)

    elif request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('customers:passport_list'))
        return HttpResponseRedirect(reverse_lazy('customers:passport_list'))


def passport_detail(request, pk):

    if request.method == 'GET':
        passport = Passport.objects.get(pk=pk)
        context = {'passport': passport,
                   'form': PassportForm(instance=passport),
                   'state_code': state_code, }
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


# ===================================================
# ==================== Customers ====================
# ===================================================


class CustomerList(ListView):
    model = Customer
    template_name = 'customers/customer-list.html'


def customer_create(request):

    if request.method == 'GET':
        context = {'form': CustomerForm, }
        return render(request, 'customers/customer-detail.html', context)

    elif request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('customers:customer_list'))
        return HttpResponseRedirect(reverse_lazy('customers:customer_list'))


def customer_detail(request, pk):

    if request.method == 'GET':
        customer = Customer.objects.get(pk=pk)
        context = {'customer': customer,
                   'form': CustomerForm(instance=customer), }
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
