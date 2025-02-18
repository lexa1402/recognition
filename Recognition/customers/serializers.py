from customers.models import Customer, Passport, PassportScan, PageScan
from rest_framework import serializers


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'middle_name', 'last_name', ]


class PassportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Passport
        fields = ['customer_ID', 'citizenship', 'birth_date', 'document_ID', 'expire_date', 'birthplace', 'authority',
                  'issue_date', 'ethnicity', 'personal_number', 'page_scan', ]


class PageScanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PageScan
        fields = ['image', 'page_number', ]


class PassportScanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PassportScan
        fields = ['passport', 'page_scan', ]
