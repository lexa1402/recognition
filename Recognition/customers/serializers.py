from customers.models import Customer, Passport, PassportScan, PageScan
from rest_framework import serializers


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'middle_name', 'last_name', ]


class PassportSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)
    customer_ID = serializers.HyperlinkedRelatedField(read_only=True, view_name='customer-detail')
    gender = serializers.CharField(max_length=1)
    citizenship = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    document_ID = serializers.CharField(max_length=16)
    expire_date = serializers.DateField()
    birthplace = serializers.CharField(max_length=32)
    authority = serializers.CharField(max_length=16)
    issue_date = serializers.DateField()
    ethnicity = serializers.CharField(max_length=16)
    personal_number = serializers.IntegerField()
    # page_scan = serializers.RelatedField(source='PageScan', read_only=True)

    def create(self, validated_data):
        return Passport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.customer_ID = validated_data.get('customer_ID', instance.customer_ID)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.citizenship = validated_data.get('citizenship', instance.citizenship)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.document_ID = validated_data.get('document_ID', instance.document_ID)
        instance.expire_date = validated_data.get('expire_date', instance.expire_date)
        instance.birthplace = validated_data.get('birthplace', instance.birthplace)
        instance.authority = validated_data.get('authority', instance.authority)
        instance.issue_date = validated_data.get('issue_date', instance.issue_date)
        instance.ethnicity = validated_data.get('ethnicity', instance.ethnicity)
        instance.personal_number = validated_data.get('personal_number', instance.personal_number)
        instance.page_scan = validated_data.get('page_scan', instance.page_scan)
        instance.save()
        return instance

    class Meta:
        model = Passport
        fields = ['id', 'customer_ID', 'gender', 'citizenship', 'birth_date', 'document_ID', 'expire_date',
                  'birthplace', 'authority', 'issue_date', 'ethnicity', 'personal_number', 'page_scan', ]


class PageScanSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField()
    page_number = serializers.IntegerField()

    def create(self, validated_data):
        return PageScan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.page_number = validated_data.get('page_number', instance.page_number)

    class Meta:
        model = PageScan
        fields = ['id', 'image', 'page_number', ]


class PassportScanSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)
    passport = serializers.HyperlinkedRelatedField(read_only=True, view_name='passport-detail')
    page_scan = serializers.HyperlinkedRelatedField(read_only=True, view_name='pagescan-detail')

    def create(self, validated_data):
        return PassportScan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.passport = validated_data.get('passport', instance.passport)
        instance.page_scan = validated_data.get('page_scan', instance.page_scan)

    class Meta:
        model = PassportScan
        fields = ['id', 'passport', 'page_scan', ]
