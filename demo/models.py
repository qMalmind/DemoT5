from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


def get_name_img(instance, filename):
    return '_'.join([get_random_string(length=5), filename])


class User(AbstractUser):
    username = models.CharField(blank=False, unique=True, max_length=254)
    email = models.CharField(blank=False, unique=True, max_length=254)
    password = models.CharField(blank=False, max_length=254)

    name = models.CharField(blank=False, max_length=254)
    surname = models.CharField(blank=False, max_length=254)
    patronymic = models.CharField(blank=True, max_length=254)

    role = models.CharField(blank=False, choices=(('admin', 'администратор'), ('user', 'пользователь')), default='user',
                            max_length=254)

    def __str__(self):
        return ' '.join([self.name, self.username, self.surname])


class Product(models.Model):
    name = models.CharField(blank=False, max_length=254, verbose_name='Наименование')
    country = models.CharField(blank=False, max_length=254, verbose_name='Страна производитель')
    photo_file = models.ImageField(blank=False, verbose_name='Изображение товара', upload_to=get_name_img,
                                   max_length=254)
    price = models.DecimalField(blank=False, default=0.00, max_digits=9, decimal_places=2, verbose_name='Стоимость')
    count = models.IntegerField(blank=False, default=1, verbose_name='Количество на складе')
    year = models.IntegerField(blank=False, default=2022, verbose_name='Год производства')
    date = models.DateField(blank=False, auto_now_add=True, verbose_name='Дата поступления на склад')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория товара')

    def __str__(self):
        return ' '.join([self.name, str(self.price)])


class Category(models.Model):
    name = models.CharField(blank=False, max_length=254, verbose_name='Название категории')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.IntegerField(blank=False, default=1)

    def __str__(self):
        return ' '.join([str(self.product), str(self.count)])


class OrderInItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(blank=False, default=1, verbose_name='Количество')
    price = models.DecimalField(blank=False, default=0.00, max_digits=9, decimal_places=2, verbose_name='Стоимость')


class Order(models.Model):
    STATUS_CHOICE = (('confirm', 'подтверждённый'), ('new', 'новый'), ('canceled', 'отменённый'))
    date = models.DateTimeField(auto_now_add=True, blank=False, verbose_name='Дата создания заказа')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    reject_reason = models.TextField(blank=True, verbose_name='Причина отказа')
    status = models.CharField(blank=False,
                              choices=STATUS_CHOICE,
                              default='new',
                              max_length=254)
    product = models.ManyToManyField(Product, related_name='orders', through=OrderInItem)

    def count_product(self):
        counter = 0
        itemInOrder = OrderInItem.objects.filter(order_id=self.id).all()

        for item in itemInOrder:
            counter += item.count

    def status_verbose(self):
        return dict(self.STATUS_CHOICE)[self.status]

    def __str__(self):
        return str(self.date)
