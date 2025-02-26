from django import forms


class PageScanForm(forms.Form):
    image = forms.ImageField()
