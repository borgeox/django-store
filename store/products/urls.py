from django.urls import path

from products.views import products, add_to_cart, remove_from_cart


app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('/category/<int:category_id>', products, name='category'),
    path('cart/add/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:order_id>', remove_from_cart, name='remove_from_cart'),

]
