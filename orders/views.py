from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from cart.cart import CartLogic
from ecomm.models import Product
from .liqpay_controller import LiqpayChekout, LiqpayCallback
from django.views import View
from .models import (
    Country,
    OrderItem,
    PaymentMethod,
    Region,
    City,
    Order)


class OrderCreate(View):

    def get(self, request):
        cart = CartLogic(request)
        form_create = OrderCreateForm()
        return render(
            request,
            "orders/order/create.html",
            context={
                "cart": cart,
                "form_create": form_create,
            },
        )

    def post(self, request):
        cart = CartLogic(request)
        data = request.POST
        form_create = OrderCreateForm(data)
        if form_create.is_valid():
            order = form_create.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            if data['payment_method'] != "2":
                return redirect('/orders/thank')
        return redirect('/orders/created')


# def order_create(request):
#     cart = CartLogic(request)
#
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          product=item['product'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             return redirect('/orders/created')
#
#     else:
#         form = OrderCreateForm
#
#     return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def order_created(request):
    cart = CartLogic(request)
    total_price = int(cart.get_total_price())

    liqpay = LiqpayChekout(total_price)
    liqpay.set_order_id()
    data = liqpay.create_param_checkout()[0]
    signature = liqpay.create_param_checkout()[1]

    return render(request, 'orders/order/created.html', {'data': data, 'signature': signature})


def thanks_page(request):
    cart = request.session['cart']

    liqpay_callback = LiqpayCallback()
    res = liqpay_callback.send_request()
    status = liqpay_callback.get_response_status(res)

    if status != 'success':
        status_error = True

        return render(request, 'orders/order/thanks.html', {"status": status_error})

    else:

        request.session['cart'] = {}
        request.session['counter_items'] = 0

        for key, value in cart.items():
            product = Product.objects.get(pk=key)
            product.quantity -= value['quantity']
            product.save()

        order = Order.objects.order_by('-id')[:1].get()
        order.paid = True
        order.save()

    return render(request, 'orders/order/thanks.html')


def get_tanks_page(request):
    return render(request, 'orders/order/thank.html')


def get_country(request):
    delivery_method_id = request.GET.get("method")
    countries = Country.objects.filter(method=delivery_method_id).order_by("country")
    return render(request, "selection/country.html", {"countries": countries})


def get_region(request):
    delivery_country_id = request.GET.get("country")
    regions = Region.objects.filter(country=delivery_country_id).order_by("region")
    return render(request, "selection/regions.html", {"regions": regions})


def get_city(request):
    delivery_region_id = request.GET.get("region")
    cities = City.objects.filter(region=delivery_region_id).order_by("city")
    return render(request, "selection/cities.html", {"cities": cities})


def get_pay_method(request):
    pay_method_id = request.GET.get("pay_method")
    pay_methods = PaymentMethod.objects.filter(delivery_method=pay_method_id).order_by(
        "method"
    )
    return render(request, "selection/pay_methods.html", {"pay_methods": pay_methods})
