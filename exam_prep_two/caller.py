import os


import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, F, When, Case
from main_app.models import Profile, Order, Product


def get_profiles(search_string=None):
    if search_string is None:
        return ''

    query = Q(full_name__icontains=search_string) \
            | Q(email__icontains=search_string)\
            | Q(phone_number__icontains=search_string)\

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles.exists():
        return ''

    result = []

    [result.append(f"Profile: {p.full_name}, email: {p.email}, "
                   f"phone number: {p.phone_number}, orders: {p.orders.count()}") for p in profiles]

    return '\n'.join(result)


def get_loyal_profiles():
    regular_cust = Profile.objects.get_regular_customers()

    if not regular_cust.exists():
        return ''

    result = []

    [result.append(f"Profile: {c.full_name}, orders: {c.orders.count()}") for c in regular_cust]

    return '\n'.join(result)


def get_top_products():
    top_products = Product.objects.annotate(
        orders_count=Count('order')
    ).filter(
        orders_count__gt=0,
    ).order_by(
        '-orders_count',
        'name'
    )[:5]

    if not top_products.exists():
        return ""

    product_lines = "\n".join(f"{p.name}, sold {p.orders_count} times" for p in top_products)

    return f"Top products:\n" + product_lines


def apply_discounts():
    updated_orders_count = Order.objects.annotate(
        products_count=Count('products')
    ).filter(
        products_count__gt=2,
        is_completed=False
    ).update(
        total_price=F('total_price') * 0.90
    )

    return f"Discount applied to {updated_orders_count} orders."


def complete_order():
    order = Order.objects.filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ""

    for product in order.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return "Order has been completed!"
