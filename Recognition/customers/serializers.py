from rest_framework import serializers

from customers.models import Customer, Passport, PageScan


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)
    passport = serializers.HyperlinkedRelatedField(view_name='passport-detail', queryset=Passport.objects.all())

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
    optional_data_1 = serializers.CharField(max_length=14, allow_null=True)
    optional_data_2 = serializers.CharField(max_length=14, allow_null=True)
    page_scan = serializers.HyperlinkedRelatedField(many=True,
                                                    view_name='pagescan-detail',
                                                    queryset=PageScan.objects.all().order_by('-id'))

    def create(self, validated_data):
        instance = Passport.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        for attr in self.Meta.fields:
            if attr not in ('url', 'page_scan'):
                setattr(instance, attr, validated_data.get(attr, getattr(instance, attr)))
        instance.save()
        return instance

    class Meta:
        model = Passport
        fields = ['url', 'id', 'issuer_code', 'surname', 'given_name', 'document_number', 'nationality_code',
                  'birth_date', 'sex', 'expiry_date', 'optional_data_1', 'optional_data_2', 'page_scan', ]
