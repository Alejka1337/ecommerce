from django import template
from ecomm.models import *

register = template.Library()


# @register.inclusion_tag('sidebar.html')
# def get_sidebar_info(products, *args, **kwargs):
#
#     specification = []
#     size = []
#     color = []
#     brand = []
#     country = []
#     material = []
#
#     spec_size = list(ProductSpecificationValue.objects.filter(specification_id=1).distinct().values('value'))
#     spec_color = list(ProductSpecificationValue.objects.filter(specification_id=2).distinct().values('value'))
#     spec_brand = list(ProductSpecificationValue.objects.filter(specification_id=3).distinct().values('value'))
#     spec_country = list(ProductSpecificationValue.objects.filter(specification_id=4).distinct().values('value'))
#     spec_material = list(ProductSpecificationValue.objects.filter(specification_id=5).distinct().values('value'))
#
#     for product in products:
#         spec = product.productspecificationvalue_set.all()
#
#         for s in spec:
#             if s.specification not in specification:
#                 specification.append(s.specification)
#
#             for sp_size in spec_size:
#                 if s.value == sp_size['value'] and s.value not in size:
#                     size.append(s.value)
#
#             for sp_color in spec_color:
#                 if s.value == sp_color['value'] and s.value not in color:
#                     color.append(s.value)
#
#             for sp_brand in spec_brand:
#                 if s.value == sp_brand['value'] and s.value not in brand:
#                     brand.append(s.value)
#
#             for sp_material in spec_material:
#                 if s.value == sp_material['value'] and s.value not in material:
#                     material.append(s.value)
#
#             for sp_country in spec_country:
#                 if s.value == sp_country['value'] and s.value not in country:
#                     country.append(s.value)
#
#     return {'specification': specification,
#             'colors': color,
#             'size': size,
#             'brand': brand,
#             'material': material,
#             'country': country,
#             'product': product}


@register.inclusion_tag('sidebar.html')
def get_sidebar_info(products):

    specification_list = set()
    size_list = set()
    color_list = set()
    brand_list = set()
    country_list = set()
    material_list = set()

    for product in products:
        product_specification = product.productspecificationvalue_set.all()
        for spec in product_specification:
            if spec.specification not in specification_list:
                specification_list.add(spec.specification)

            if spec.specification_id == 1:
                size_list.add(spec.value)

            elif spec.specification_id == 2:
                color_list.add(spec.value)

            elif spec.specification_id == 3:
                brand_list.add(spec.value)

            elif spec.specification_id == 4:
                country_list.add(spec.value)

            elif spec.specification_id == 5:
                material_list.add(spec.value)

    return {'specifications': specification_list,
            'colors': color_list,
            'sizes': size_list,
            'brands': brand_list,
            'materials': material_list,
            'countries': country_list,
            'product': product}