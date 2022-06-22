from django.core import validators
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from demo.forms import RegisterUserForm
from demo.models import Product, Category, Cart, User, Order, OrderInItem


class RegisterUserView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


def check_login(request):
    user = User.objects.filter(username=request.GET.get('login'))
    if user:
        return JsonResponse({
            'errors': 'Login not unique'
        })

    return JsonResponse({
        'success': 'Login success'
    })


def check_email(request):
    email = request.GET.get('email')

    try:
        validators.validate_email(email)
    except ValidationError as error:
        response = {
            'is_valid': False
        }
    else:
        response = {
            'is_valid': True,
            'is_taken': bool(User.objects.filter(email=email).first())
        }

    return JsonResponse(response)


def catalog(request):
    filter_product = request.GET.get('filter')
    if filter_product:
        products = Product.objects.filter(category__id=filter_product).all()
    else:
        products = Product.objects.all()

    order_by = request.GET.get('order_by')

    if order_by:
        products = products.order_by(order_by)
    else:
        products = products.order_by('-date')

    category = Category.objects.all()

    return render(request, 'demo/catalog.html', context={
        'products': products,
        'category': category,
    })


def product(request, pk):
    product = Product.objects.filter(id=pk).first()

    return render(request, 'demo/product.html', context={
        'product': product,
    })


def cart(request):
    carts = Cart.objects.filter(user=request.user).all()
    return render(request, 'demo/cart.html', context={'carts': carts})


def add_cart(request):
    product = Product.objects.filter(id=request.GET.get('product')).first()
    cart = Cart.objects.filter(user=request.user, product=product).first()

    if cart:
        if cart.count + 1 > product.count:
            return JsonResponse({
                'error': "Can't add more"
            })

        cart.count += 1
        cart.save()

        return JsonResponse({
            'count': cart.count
        })
    cart = Cart.objects.create(user=request.user, product=product, count=1)

    return JsonResponse({
        'count': cart.count
    })


def dif_cart(request):
    product = Product.objects.filter(id=request.GET.get('product')).first()
    cart = Cart.objects.filter(user=request.user, product=product).first()

    if cart:
        if cart.count - 1 <= 0:
            cart.delete()
            return JsonResponse({
                'error': "belove zero"
            })
        cart.count -= 1
        cart.save()

        return JsonResponse({
            'count': cart.count
        })

    return JsonResponse({
        'error': "Product not found"
    })


def create_order(request):
    check_password = request.user.check_password(request.GET.get('password'))

    if check_password:
        items_cart = Cart.objects.filter(user=request.user).all()

        if items_cart:
            order = Order.objects.create(user=request.user)

            print(order.status_verbose())

            for item in items_cart:
                item_in_order = OrderInItem.objects.create(order=order, product=item.product, count=item.count,
                                                           price=item.product.price * item.count)
                item.delete()

            return JsonResponse({
                'success': 'Order create'
            })
        else:
            return JsonResponse({
                'error': 'Void cart'
            })

    return JsonResponse({
        'invalid_password': 'invalid password'
    })


def orders(request):
    order = Order.objects.filter(user=request.user).all()
    return render(request, 'demo/order.html', context={'orders': order})


def delete_order(request, pk):
    order = Order.objects.filter(user=request.user, id=pk)
    if order:
        order.delete()

    return redirect(reverse_lazy('orders'))



def contact_company(request):
    return render(request, 'demo/contact.html')


def about(request):
    return render(request, 'demo/about.html', context={'products': Product.objects.order_by('-date')[:5]})
