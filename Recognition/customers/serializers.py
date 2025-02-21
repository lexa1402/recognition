from rest_framework import serializers

from customers.models import Customer, Passport, PageScan


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)
    passport = serializers.HyperlinkedRelatedField(read_only=True, view_name='passport-detail')

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.passport = validated_data.get('passport', instance.passport)
        instance.save()
        return instance

    class Meta:
        model = Customer
        fields = ['url', 'id', 'passport', ]


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
        fields = ['url', 'id', 'image', 'page_number', ]


class PassportSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)
    issuer_code = serializers.CharField(max_length=32, allow_null=True)
    surname = serializers.CharField(max_length=32, allow_null=True)
    given_name = serializers.CharField(max_length=16, allow_null=True)
    document_number = serializers.CharField(max_length=9, allow_null=True)
    nationality_code = serializers.CharField(max_length=32, allow_null=True)
    birth_date = serializers.DateField(allow_null=True)
    sex = serializers.CharField(max_length=1, allow_null=True)
    expiry_date = serializers.DateField(allow_null=True)
    optional_data = serializers.CharField(max_length=14, allow_null=True)
    page_scan = serializers.HyperlinkedRelatedField(many=True, view_name='pagescan-detail', queryset=PageScan.objects.all())

    def create(self, validated_data):
        instance = Passport.objects.create(**validated_data)
        return instance

    # Fix here: Setup Update of Validated Data
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.issuer_code = validated_data.get('issuer_code', instance.issuer_code)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.given_name = validated_data.get('given_name', instance.given_name)
        instance.document_number = validated_data.get('document_number', instance.document_number)
        instance.nationality_code = validated_data.get('nationality_code', instance.nationality_code)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.expiry_date = validated_data.get('expiry_date', instance.expiry_date)
        instance.optional_data = validated_data.get('optional_data', instance.optional_data)
        instance.save()
        return instance

    class Meta:
        model = Passport
        fields = ['url', 'id', 'issuer_code', 'surname', 'given_name', 'document_number', 'nationality_code',
                  'birth_date', 'sex', 'expiry_date', 'optional_data', 'page_scan']
