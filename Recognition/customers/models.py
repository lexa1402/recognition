from django.db import models


class Customer(models.Model):

    passport = models.ForeignKey('Passport', on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        passport = Passport.objects.get(pk=self.passport.id)
        return f'{passport.surname} {passport.given_name}'

    class Meta:
        app_label = 'customers'
        db_table = 'customer'
        verbose_name = 'Customer'


class Passport(models.Model):

    issuer_code = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    given_name = models.CharField(max_length=16)
    document_number = models.CharField(max_length=9)
    nationality_code = models.CharField(max_length=32)
    birth_date = models.DateField()
    sex = models.CharField(choices=[('m', 'M'), ('f', 'F')], default='M', max_length=1)
    expiry_date = models.DateField()
    optional_data = models.CharField(max_length=14)
    page_scan = models.ManyToManyField('PageScan')
    objects = models.Manager()

    def __str__(self):
        return f'{self.surname} {self.given_name}'

    class Meta:
        app_label = 'customers'
        db_table = 'passport'
        verbose_name = 'Passport'


class PageScan(models.Model):
    image = models.ImageField()
    page_number = models.PositiveIntegerField()
    objects = models.Manager()

    def __str__(self):
        try:
            passport = Passport.objects.filter(page_scan=self)[0]
            return f'{passport.surname} {passport.given_name} ({self.page_number} стр.)'
        except IndexError:
            return f'[ Unknown Scan {self.id} ]'

    class Meta:
        app_label = 'customers'
        db_table = 'pagescan'
        verbose_name = 'Page Scan'
