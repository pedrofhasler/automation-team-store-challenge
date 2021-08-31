from os import name
from django import forms
from django.contrib import admin
from django.core.checks import messages
from django.db.models import fields
from django.urls import path, reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product
import pandas as pd
import urllib.request

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created", "modified"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "category",
        "price",
        "is_available",
        "created",
        "modified",
    ]
    list_filter = ["is_available", "created", "modified"]
    list_editable = ["price", "is_available"]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):  

        if request.method == 'POST':
            csv_file = request.FILES['csv_upload']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            csv_data = pd.read_csv(csv_file)
            print(csv_data.iloc[0])
            count_row = csv_data.shape[0]
            for i in range(0, count_row):
                category = Category.objects.update_or_create(
                    name = csv_data.iloc[i]['brand'],
                )
                
                img_name = csv_data.iloc[i]['img'].split('/p/')
                img_path_to_save = '{}{}{}'.format('media/products/', img_name[1][:60],'.jpg')
                img_path_to_open = '{}{}{}'.format('products/', img_name[1][:30],'.jpg')

                #conflito com characteres especiais, não estou conseguindo achar a causa
                try:
                    urllib.request.urlretrieve(csv_data.iloc[i]['img'], img_path_to_save)
                except:
                    img_path_to_open = 'products/no_image.jpg'
                    pass

                #price
                price_string = csv_data.iloc[i]['price'].split(',')
                price_string[0] = price_string[0][3:]
                price = float(price_string[0]+"."+price_string[1])

                created = Product.objects.update_or_create(
                    name = csv_data.iloc[i]['name'][:40],
                    category = category[0],
                    price = price,
                    description = csv_data.iloc[i]['description'],
                    image = img_path_to_open,
                    url = csv_data.iloc[i]['url']
                    )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)    

        form = CsvImportForm()
        data = {'form': form}
        return render(request, 'admin/csv_upload.html', data)