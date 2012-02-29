from django.contrib import admin
from django import forms
from seo import models
from seo.models import MetaData
from django.conf import settings

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MetaData
        widgets = {
            'regular_expression': forms.RadioSelect
        }

class MetaDataAdmin(admin.ModelAdmin):

    form = MyModelForm
    
    list_display = ('path', 'regular_expression', )
    search_fields = ('path', )
    list_filter = ['regular_expression']

admin.site.register(models.MetaData, MetaDataAdmin)
