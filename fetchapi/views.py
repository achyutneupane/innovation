from django.shortcuts import render
from .models import *
import json

import requests

def index(request):
    apiUrl = 'https://raw.githubusercontent.com/younginnovations/internship-challenges/master/programming/petroleum-report/data.json'
    response = requests.get(apiUrl)
    apidatas = json.loads(response.content.decode('utf-8'))
    for apidata in apidatas:
        year = (apidata['year'])
        petroleum_product = apidata['petroleum_product']
        sale = apidata['sale']
        obj, created = Products.objects.get_or_create(year=year, petroleum_product=petroleum_product, sale=sale)
    data = {
        'contents': apidatas,
        'content': Products.objects.all()
    }
    return render(request, 'index.html', data)

def result(request):
    petroleum_products = Products.objects.values_list('petroleum_product',flat=True).distinct()
    resultdata = []
    dataset = Products.objects.all().order_by('-year')
    for j in range(len(petroleum_products)):
        count=0
        c =0
        first_loop=True
        total_sale=0
        max=0
        min=0
        for i,datas in enumerate(dataset):
            if(petroleum_products[j]==datas.petroleum_product):
                if(first_loop):
                    first = int(datas.year)
                last = int(datas.year)
                if (last == first - 5):
                    resultdata.append([petroleum_products[j], str(last+1) + "-" + str(last + 5),min, max, total_sale/(1 if count==0 else count)])
                    total_sale = 0
                    count=0
                    first = last
                    max = 0
                    min = datas.sale
                count = count + 1  if datas.sale != 0 else count
                total_sale = total_sale + datas.sale
                max = max if max>datas.sale else datas.sale
                min = datas.sale if min==0 else (min if min<datas.sale else datas.sale)
                first_loop=False
        count=1 if count==0 else count
        resultdata.append([petroleum_products[j], str(last) + "-" + str(last+4),min, max,total_sale/ count])
    data = {
        'productname': resultdata
    }
    return render(request, 'output.html', data)
