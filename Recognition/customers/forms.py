from django import forms
from django.db.models import Q

from customers.models import Passport, Customer, PageScan


class PageScanForm(forms.Form):
    image = forms.ImageField()


class PassportForm(forms.ModelForm):
    
    page_scan = forms.ModelMultipleChoiceField(queryset=PageScan.objects.filter(~Q(mrz_text=None)).order_by('-id'),
                                               required=True)

    class Meta:
        model = Passport
        fields = ['page_scan', ]


class CustomerForm(forms.ModelForm):

    passport = forms.ModelChoiceField(queryset=Passport.objects.all().order_by('-id'),
                                      required=True)

    class Meta:
        model = Customer
        fields = ['passport', 'address', 'phone_number', 'email', ]


class CustomerListForm(forms.Form):
    is_checked = forms.ModelMultipleChoiceField(queryset=Customer.objects.all(),
                                                required=False,
                                                widget=forms.CheckboxSelectMultiple)


class PassportListForm(forms.Form):
    is_checked = forms.ModelMultipleChoiceField(queryset=Passport.objects.all(),
                                                required=False,
                                                widget=forms.CheckboxSelectMultiple)


class PageScanListForm(forms.Form):
    is_checked = forms.ModelMultipleChoiceField(queryset=PageScan.objects.all(),
                                                required=False,
                                                widget=forms.CheckboxSelectMultiple)
