from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from cart.form import CartAddProductForm
from shop.settings import GOOGLE_MAPS_API_KEY
from comments.form import CommentForm


def homepage(request):
    products = Product.objects.filter(available=True)
    context = {'products': products,
               'title': 'Главная страница'}

    return render(request, 'ecomm/main.html', context=context)


def category_page(request, slug):
    category = Category.objects.get(slug=slug)

    if category.level == 0:
        child_cat = category.children.all()
        context = {'category': category, 'child_cat': child_cat}
        return render(request, 'ecomm/category_parent.html', context=context)

    else:
        products = category.product_set.all()
        context = {
            'products': products,
            'category': category}

        sort = request.GET.get('sort')
        if sort:
            products = category.product_set.all()[:int(sort)]
            context['products'] = products

        order_min = request.GET.get('order_min')
        if order_min:
            products = category.product_set.all().order_by('price')
            context['products'] = products

        order_max = request.GET.get('order_max')
        if order_max:
            products = category.product_set.all().order_by('-price')
            context['products'] = products

        return render(request, 'ecomm/category_children.html', context=context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, pk=id, slug=slug, available=True)
    category = product.category
    cart_product_form = CartAddProductForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.save(commit=False)
            data.product_id = product.pk
            data.save()
            return redirect('ecomm:product_detail', id=id, slug=slug)
    else:
        comment_form = CommentForm()

    context = {'product': product,
               'cart_product_form': cart_product_form,
               'comment_form': comment_form,
               'similar_product': category.product_set.all()[:5]}

    return render(request, 'ecomm/product.html', context=context)


def feedback(request):
    return render(request, 'ecomm/feedback.html', {'title': 'Обратная связь',
                                                   'myapi': GOOGLE_MAPS_API_KEY})


def policy(request):
    return render(request, 'ecomm/policy.html', {'title': 'Политика Конфеденциальности'})


def shipping_and_payment(request):
    return render(request, 'ecomm/shipping_and_payment.html', {'title': 'Доставка и оплата'})


def about(request):
    return render(request, 'ecomm/about.html', {'title': 'О сайте'})



