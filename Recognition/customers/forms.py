from django import forms

from customers.models import Passport


class PageScanForm(forms.Form):
    image = forms.ImageField()


class PassportForm(forms.ModelForm):
    # issuer_code = forms.CharField(max_length=3)
    # surname = forms.CharField(max_length=32)
    # given_name = forms.CharField(max_length=32)
    # document_number = forms.CharField(max_length=9)
    # nationality_code = forms.CharField(max_length=3)
    # birth_date = forms.DateField()
    # sex = forms.CharField(max_length=1)
    # expiry_date = forms.DateField()
    # optional_data_1 = forms.CharField(max_length=14, required=False)
    # optional_data_2 = forms.CharField(max_length=14, required=False)

    class Meta:
        model = Passport
        fields = ['issuer_code', 'surname', 'given_name', 'document_number', 'nationality_code', 'birth_date', 'sex',
                  'expiry_date', 'optional_data_1', 'optional_data_2', ]
