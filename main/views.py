#standerd
import datetime
#django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
#local
from main.decorators import role_required
# from customers.models import *
# from product.models import *
# from orders.models import *

# Create your views here.
# @check_mode

@login_required
def app(request):

    return HttpResponseRedirect(reverse('main:index'))


@login_required
@role_required(['superadmin'])
def index(request):
    today = datetime.date.today()

    # product_count = Product.objects.filter(is_deleted = False).count()
    # customers_count = Customer.objects.filter(is_deleted = False).count()
    # order_count = OrderItem.objects.filter(is_deleted = False).count()
    # orders_today = OrderItem.objects.filter(is_deleted=False,date_added__date=today).count()
    # customers_today = Customer.objects.filter(is_deleted=False,date_added__date=today).count()
    # products_today = Product.objects.filter(is_deleted=False,date_added__date=today).count()
    # total_sales = OrderItem.objects.filter(is_deleted=False,order_status='delivered').count()

    # recent_orders = OrderItem.objects.filter(is_deleted=False).order_by('-date_added')[:5]
    # recent_customers = Customer.objects.filter(is_deleted=False).order_by('-date_added')[:5]
    # recent_products = Product.objects.filter(is_deleted=False).order_by('-date_added')[:5]

    context = {
        'page_name' : 'Dashboard',
        # 'product_count' : product_count,
        # 'customers_count' : customers_count,
        # 'order_count' : order_count,
        # 'customers_today' :customers_today,
        # 'products_today' :products_today,
        # 'orders_today' :orders_today,
        # 'total_sales' : total_sales,

        # 'recent_orders' : recent_orders,
        # 'recent_customers' : recent_customers,
        # 'recent_products' : recent_products,

    }

    return render(request,'admin_panel/index.html', context)
