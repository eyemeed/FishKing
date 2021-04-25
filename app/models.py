from django.db import models

# Create your models here.
class Category(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name='Mã')
    name = models.CharField(max_length=200, verbose_name='Tên loại sản phẩm')
    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=30,  unique=True, verbose_name='Mã')
    name = models.CharField(max_length=200, verbose_name='Tên sản phẩm')
    description = models.CharField(max_length=1000,  blank=True, verbose_name='Miêu tả')
    price = models.FloatField(verbose_name='Giá')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Loại sản phẩm')
    image = models.ImageField(upload_to='assets/img/product', verbose_name='Ảnh')
    def __str__(self):
        return self.name

class Order(models.Model):
    class Status:
        NEW = 0
        DELIVERED = 1
        CANCELED = 2

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Sản phẩm')
    qty = models.IntegerField(verbose_name='Số lượng')
    customer_name = models.CharField(max_length=50, verbose_name='Tên khách hàng')
    customer_phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    customer_address = models.CharField(max_length=200, verbose_name='Địa chỉ')
    order_date = models.DateTimeField(verbose_name='Ngày đặt hàng')
    deliver_date = models.DateTimeField(null=True, verbose_name='Ngày giao hàng')
    status = models.IntegerField(verbose_name='Tình trạng')

    @property
    def total(self):
        return self.qty * self.product.price