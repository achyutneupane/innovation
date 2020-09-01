from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Avg, Min, Max
import json

import requests


# Create your views here.
def index(request):
    apiUrl = 'https://raw.githubusercontent.com/younginnovations/internship-challenges/master/programming/petroleum-report/data.json'
    response = requests.get(apiUrl)
    apidatas = json.loads(response.content.decode('utf-8'))
    print(apidatas)
    for apidata in apidatas:
        year = (apidata['year'])
        petroleum_product = apidata['petroleum_product']
        sale = apidata['sale']
        # newdata = Products(year=year, petroleum_product=petroleum_product, sale=sale)
        # newdata.save()

    data = {
        'contents': apidatas,
        'content': Products.objects.all()
    }

    return render(request, 'index.html', data)


def result(request):

    petroleum_products = Products.objects.values_list('petroleum_product',flat=True).distinct()
    print(petroleum_products[0])
    avg=0
    count= 0
    petrolsale = []
    resultdata = []
    testdata = []
    total_sale=0
    max=0
    dataset = Products.objects.all().order_by('year')
    for j in range(len(petroleum_products)):
        count=0
        first_loop=True
        total_sale=0
        max=0
        min =0
        for i,datas in enumerate(dataset):
            if(petroleum_products[j]==datas.petroleum_product and datas.sale!=0):
                if(first_loop):
                    first = int(datas.year)
                last = int(datas.year)
                if (last == first + 5):
                    resultdata.append([petroleum_products[j], str(first) + "-" + str(last - 1),min, max, total_sale /count])
                    total_sale = 0
                    count=0
                    first = last
                total_sale = total_sale + datas.sale
                max=max if max>datas.sale else datas.sale
                min = min if min > datas.sale else datas.sale
                count = count + 1
                first_loop=False
        resultdata.append([petroleum_products[j], str(first) + "-" + str(last),min, max,total_sale / count])
    data = {
        'productname': resultdata
    }
    return render(request, 'output.html', data)
