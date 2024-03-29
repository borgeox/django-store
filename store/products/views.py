from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from products.models import Product, ProductCategory, CartItem
from users.models import User


# views = контроллеры = обработчики запросов = функции = вьюхи

def index(request):
    context = {'title': 'Store'}
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    products_to_show = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    products_to_show.order_by('id')

    paginator = Paginator(products_to_show, per_page=3)
    page_number = request.GET.get('page', 1)
    products_page = paginator.get_page(page_number)
    page_numbers = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=0)

    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_page,
        'page_numbers': page_numbers,
    }
    return render(request, 'products/products.html', context)


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_items = CartItem.objects.filter(user=request.user, product=product)

    if cart_items:
        cart_item = cart_items.first()
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(user=request.user, product=product, quantity=1)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_cart(request, order_id):
    cart_item = CartItem.objects.get(id=order_id)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
