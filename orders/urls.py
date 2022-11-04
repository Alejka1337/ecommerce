from django.urls import re_path, path
from . import views


urlpatterns = [
    # re_path(r'^create/$', views.order_create, name='order_create'),
    path('create/', views.OrderCreate.as_view(), name='order_create'),
    path("ajax/load_country", views.get_country, name="ajax_load_countries"),
    path("ajax/load_regions", views.get_region, name="ajax_load_regions"),
    path("ajax/load_cities", views.get_city, name="ajax_load_cities"),
    path("ajax/load_pay_methods", views.get_pay_method, name="ajax_load_pay_methods"),
    path('created/', views.order_created, name='order_created'),
    path('thanks/', views.thanks_page, name='thanks_page'),
    path('thank/', views.get_tanks_page, name='thank_page'),

]