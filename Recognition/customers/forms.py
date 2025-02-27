from django import forms

from customers.models import Passport, Customer


class PageScanForm(forms.Form):
    image = forms.ImageField()


class PassportForm(forms.ModelForm):

    class Meta:
        model = Passport
        fields = ['issuer_code', 'surname', 'given_name', 'document_number', 'nationality_code', 'birth_date', 'sex',
                  'expiry_date', 'optional_data_1', 'optional_data_2', ]


class CustomerForm(forms.ModelForm):

    passport = forms.ModelChoiceField(queryset=Passport.objects.all(), required=True)

    class Meta:
        model = Customer
        fields = ['passport', 'address', 'phone_number', 'email', ]
