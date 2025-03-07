from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms import ModelForm

from customers.models import Customer, Passport, PageScan


class PageScanForm(ModelForm):
    class Meta:
        model = PageScan
        fields = '__all__'


class PageScanInline(admin.TabularInline):
    model = Passport.page_scan.through
    form = PageScanForm
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        return format_html(f'<img src="{obj.pagescan.image.url}" width="100px" height="auto"/>')

    preview.short_description = "Preview"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = ['passport', 'address', 'phone_number', 'email', ]


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    fields = ['issuer_code', 'surname', 'given_name', 'document_number', 'nationality_code', 'birth_date', 'sex',
              'expiry_date', 'optional_data_1', 'optional_data_2', ]
    inlines = [PageScanInline]


@admin.register(PageScan)
class PageScanAdmin(admin.ModelAdmin):
    readonly_fields = ['image_preview', ]

    def image_preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width = 400 height = auto>')

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True
