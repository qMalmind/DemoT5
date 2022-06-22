from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from demo.views import *

urlpatterns = [
    path('', catalog, name='catalog'),
    path('product/<pk>', product, name='product'),
    path('cart/', cart, name='cart'),
    path('add_cart/', add_cart, name='add_cart'),
    path('dif_cart/', dif_cart, name='dif_cart'),
    path('create_order/', create_order, name='create_order'),
    path('orders/', orders, name='orders'),
    path('delete_order/<pk>', delete_order, name='delete_order'),

    path('contact/', contact_company, name='contact'),
    path('about/', about, name='about'),

    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('validate_login/', check_login, name='valid_login'),
    path('validate_email/', check_email, name='valid_email'),
    path('logout/', LogoutView.as_view(), name='logout'),
]