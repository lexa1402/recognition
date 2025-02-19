from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    owner = models.ForeignKey('auth.User', related_name='customer', on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        app_label = 'customers'


class Passport(models.Model):
    customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    gender = models.CharField(choices=[('м', 'М'), ('ж', 'Ж')], default='М', max_length=1)
    citizenship = models.CharField(max_length=32)
    birth_date = models.DateField()
    document_ID = models.CharField(max_length=16)
    expire_date = models.DateField()
    birthplace = models.CharField(max_length=32)
    authority = models.CharField(max_length=16)
    issue_date = models.DateField()
    ethnicity = models.CharField(max_length=16)
    personal_number = models.PositiveBigIntegerField()
    page_scan = models.ManyToManyField('PageScan', through='PassportScan')
    objects = models.Manager()

    def __str__(self):
        customer = Customer.objects.get(pk=self.id)
        return f'{customer.first_name} {customer.last_name}'

    class Meta:
        app_label = 'customers'
        verbose_name = 'Passport'


class PageScan(models.Model):
    image = models.ImageField()
    page_number = models.PositiveIntegerField()
    objects = models.Manager()

    def __str__(self):
        try:
            passport_scan = PassportScan.objects.get(page_scan=self)
            passport = Passport.objects.get(id=passport_scan.passport.id)
            customer = Customer.objects.get(id=passport.customer_ID.id)
            return f'{customer.first_name} {customer.last_name} ({self.page_number} стр.)'
        except PassportScan.DoesNotExist:
            return f'[Deleted Scan #{self.id}]'

    class Meta:
        app_label = 'customers'
        verbose_name = 'Page Scan'


class PassportScan(models.Model):
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE)
    page_scan = models.ForeignKey(PageScan, on_delete=models.CASCADE)
    objects = models.Manager()

    def image(self):
        page_scan = PageScan.objects.get(id=self.page_scan.id)
        return page_scan.image
