from django.shortcuts import render, HttpResponse, redirect
from .models import *
import math
from datetime import datetime
from .forms import *

# Create your views here.

PAGE_SIZE = 9  

priceList = [
    {'id': 1, 'name': 'Dưới 100,000đ', 'max': 100000},
    {'id': 2, 'name': 'Từ 100.000đ - 500.000đ', 'min': 100000, 'max': 500000},
    {'id': 3, 'name': 'Từ 500.000đ - 1.000.000đ', 'min': 500000, 'max': 1000000},
    {'id': 4, 'name': 'Từ 1.000.000đ - 10.000.000đ', 'min': 1000000, 'max': 10000000},
    {'id': 5, 'name': 'Trên 10.000.000đ', 'min': 10000000},
]

def index(request):
    return render(request, 'index.html')

def product(request):
    name = request.GET.get('name', '')
    categoryId = request.GET.get('categoryId')    
    productList = Product.objects.filter(name__icontains=name)    
    categoryId = int(categoryId) if categoryId else None

    if categoryId:
        productList = productList.filter(category__id=categoryId)
    
    priceId = request.GET.get('priceId')
    priceId = int(priceId) if priceId else None
    price = priceList[priceId-1] if priceId else {}
    minPrice, maxPrice = price.get('min'), price.get('max')

    if minPrice: 
        productList = productList.filter(price__gte=minPrice)

    if maxPrice:
        productList = productList.filter(price__lte=maxPrice)

    page = request.GET.get('page', '')
    page = int(page) if page.isdigit() else 1
    start = (page-1)*PAGE_SIZE
    end = start + PAGE_SIZE
    total = len(productList)
    num_page = math.ceil(total/PAGE_SIZE)

    categoryList = Category.objects.all()
    context = {
        'priceList': priceList,
        'categoryList': categoryList,
        'productList': productList[start:end],
        'name': name,
        'categoryId': categoryId or '',
        'priceId': priceId or '',
        'page': page, 'start': start, 'end': end, 'total': total,
        'num_page': num_page
    }

    return render(request, 'product.html', context)

def viewProductDetail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'product-detail.html', context)

def orderProduct(request, pk):
    product = Product.objects.get(pk=pk)
    form = OrderForm(initial={'qty': 1})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #print('data=', data)
            order = Order()
            order.product = product
            order.qty = data['qty']
            order.customer_name = data['customer_name']
            order.customer_phone = data['customer_phone']
            order.customer_address = data['customer_address']
            order.order_date = datetime.now()
            order.status = Order.Status.NEW
            order.save()
            return redirect('/success')

    context = {'form': form, 'product': product}
    return render(request, 'order.html', context)

def success(request):
    return render(request, 'success.html')