from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.conf import settings
import math

PAGE_SIZE = 10

priceList = [
    {'id': 1, 'name': 'Dưới 100,000đ', 'max': 100000},
    {'id': 2, 'name': 'Từ 100.000đ - 500.000đ', 'min': 100000, 'max': 500000},
    {'id': 3, 'name': 'Từ 500.000đ - 1.000.000đ', 'min': 500000, 'max': 1000000},
    {'id': 4, 'name': 'Từ 1.000.000đ - 10.000.000đ', 'min': 1000000, 'max': 10000000},
    {'id': 5, 'name': 'Trên 10.000.000đ', 'min': 10000000},
]

@login_required
def staffHome(request):
    return render(request, 'staff/home.html')

@login_required
def listCategory(request):
    page = request.GET.get('page', '')
    page = int(page) if page.isdigit() else 1
    pageSize = settings.PAGE_SIZE
    start = (page-1)* pageSize
    end = start + pageSize

    categoryList = Category.objects.all()
    total = categoryList.count()

    context = {
        'categoryList': categoryList[start:end],
        'start': start,
        'page': page,
        'total': total,
        'numpage': math.ceil(total/pageSize)
    }
    
    return render(request, 'staff/category/list.html', context)

@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    success_url = '/staff'
    template_name = 'staff/category/form.html'

@method_decorator(login_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    success_url = '/staff'
    template_name = 'staff/category/form.html'

@login_required
def deleteCategory(request, pk):
    c = Category.objects.get(pk=pk)
    c.delete()
    return redirect('staff-home')

@login_required
def listProduct(request):
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

    return render(request,'staff/product/list.html', context)  

@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = '/staff/list-product'
    template_name = 'staff/product/form.html'

@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    success_url = '/staff/list-product'
    template_name = 'staff/product/form.html'

@login_required
def deleteProduct(request, pk):
    p = Product.objects.get(pk=pk)
    p.delete()
    return redirect('list-product')

@login_required
def listOrder(request):
    page = request.GET.get('page', '')
    page = int(page) if page.isdigit() else 1
    pageSize = settings.PAGE_SIZE
    start = (page-1)* pageSize
    end = start + pageSize

    orderList = Order.objects.all()
    orderList = orderList.order_by('status', '-order_date')
    total = orderList.count()

    context = {
        'orderList': orderList[start:end],
        'start': start,
        'page': page,
        'total': total,
        'numpage': math.ceil(total/pageSize)
    }

    return render(request, 'staff/order/list.html', context)

@login_required
def viewOrder(request, pk):
    order = Order.objects.get(pk=pk)    
    context = {'order': order}
    return render(request, 'staff/order/detail.html', context)

@login_required
def confirmOrderDeliver(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = Order.Status.DELIVERED
    order.deliver_date = datetime.now()
    order.save()
    return redirect('list-order')

@login_required
def cancelOrder(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = Order.Status.CANCELED
    order.save()
    return redirect('list-order')

def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username = user.username, password = request.POST.get('password1'))
            login(request, user)
            return redirect('staff-home') 
    return render(request, 'registration/signup.html', {'form': form})

