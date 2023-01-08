import json
import datetime
from datetime import datetime
from main.decorators import role_required
import razorpay

from django.db.models import Q,F
from django.http import JsonResponse
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User,Group
from django.http import HttpResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from django.template.context_processors import csrf

from customer.models import Customer, CartItem, CustomerAddress, WhishlistItem
from main.functions import generate_form_errors, get_auto_id
from mechion_test.settings import CUSTOMER_LOGIN_URL, CUSTOMER_LOGOUT_URL,RZP_ID_KEY,RZP_SECRET_KEY
from order.models import Order, OrderItem
from payment.models import Payment
from product.models import Product
from web.forms import CustomerAddressForm

client = razorpay.Client(auth=(RZP_ID_KEY, RZP_SECRET_KEY))

# Create your views here.

def customer_join(request):

    context = {
        'page_name' : 'Login',
    }

    return render(request,'login.html', context)


def register_user(request):
    if not Customer.objects.filter(user=request.user,is_deleted=False).exists():
        user_data = User.objects.get(pk=request.user.pk)

        if Group.objects.filter(name="customer").exists():
            group = Group.objects.get(name="customer")
        else:
            group = Group.objects.create(name="customer")

        user_data.groups.add(group)

        Customer.objects.create(
            user=user_data,
            auto_id=get_auto_id(Customer),
            creator=user_data,
            updater=user_data,
            name=request.user.username,
            email=request.user.email,
        )

    return redirect(reverse('web:home'))


def customer_logout(request):
    logout(request)
    return redirect(reverse(CUSTOMER_LOGIN_URL))


@login_required(login_url=CUSTOMER_LOGIN_URL)
@role_required(['customer'])
def home(request):
    print(request.user.email)
    instances = Product.objects.filter(is_deleted=False,status=True)

    context = {
        "instances" : instances,
        'page_name' : 'home',
    }

    return render(request,'web/index.html', context)


@login_required(login_url=CUSTOMER_LOGIN_URL)
def product_view(request,pk):
    print(request.user.email)
    instance = Product.objects.get(pk=pk,is_deleted=False,status=True)

    context = {
        "instance" : instance,
        'page_name' : 'Product',
    }

    return render(request,'web/product.html', context)


@login_required(login_url=CUSTOMER_LOGIN_URL)
def cart(request):
    print(request.user.email)
    instances = CartItem.objects.filter(customer__user=request.user,is_deleted=False)

    context = {
        "instances" : instances,
        'page_name' : 'Cart',
    }

    return render(request,'web/cart.html', context)


@login_required(login_url=CUSTOMER_LOGIN_URL)
def add_cart(request,pk,qty):
    print(request.user.email)
    print(pk,qty)
    customer = Customer.objects.get(user=request.user,is_deleted=False)
    instance = Product.objects.get(pk=pk,is_deleted=False,status=True)
    unit_price = (int(instance.price) * int(qty))

    if not CartItem.objects.filter(customer=customer,product__pk=pk,is_deleted=False).exists():
        CartItem.objects.create(
            auto_id = get_auto_id(CartItem),
            creator = request.user,
            date_updated = datetime.today(),
            updater = request.user,

            customer = customer,
            product = instance,
            qty = qty,
            unit_price = unit_price,
        )

        response_data = {
        "status": "true",
        "title": "Successfully Added",
        "message": "Successfully Added to Cart.",
        'redirect': 'true',
        "redirect_url": reverse('web:cart')
        }
    else:
        if not qty is 0 or qty is "0":
            CartItem.objects.filter(customer=customer,product__pk=pk,is_deleted=False).update(qty=qty)

    response_data = {
        "status": "true",
        "title": "Successfully Added",
        "message": "Successfully Added to Cart.",
        'redirect': 'true',
        "redirect_url": reverse("web:product_view", kwargs={'pk':pk})
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required(login_url=CUSTOMER_LOGIN_URL)
def remove_from_cart(request,pk):
    response_data = {}

    if CartItem.objects.filter(pk=pk, customer__user=request.user, is_deleted=False).exists():
        CartItem.objects.filter(pk=pk).delete()

        response_data = {
            "status": "true",
            "action" : "removed",
            "title": "Successfully Removed",
            "message": "Product Successfully Removed From Cart.",
            "redirect": "true",
            "redirect_url": reverse('web:cart')
        }
    else:
        # print("no varient")
        response_data = {
        "status": "false",
        "title": "No Product",
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required(login_url=CUSTOMER_LOGIN_URL)
def increment_cart(request,pk):
    response_data = {}
    today = datetime.today()

    if CartItem.objects.filter(pk=pk).exists():
        instance = CartItem.objects.get(pk=pk)
        instance.qty = instance.qty + 1

        price = instance.product.price
        stock = instance.product.stock

        if instance.qty > stock :

            return redirect(reverse("web:cart"))

        else:
            product_price = price * instance.qty

            instance.unit_price = product_price
            instance.save()

            total = CartItem.objects.filter(customer__user=request.user,is_deleted=False).aggregate(total_price=Sum('unit_price'))["total_price"]

            return redirect(reverse("web:cart"))
    else:

        return redirect(reverse("web:cart"))


@login_required(login_url=CUSTOMER_LOGIN_URL)
def decrement_cart(request,pk):
    response_data = {}
    today = datetime.today()

    if CartItem.objects.filter(pk=pk).exists():
        instance = CartItem.objects.get(pk=pk)
        instance.qty = instance.qty - 1

        price = instance.product.price

        product_price = price * instance.qty


        if instance.qty == 0:
            return redirect(reverse("web:cart"))
        else:

            instance.unit_price = product_price
            instance.save()

        total = CartItem.objects.filter(customer__user=request.user,is_deleted=False).aggregate(total_price=Sum('unit_price'))["total_price"]

        return redirect(reverse("web:cart"))
    else:

        return redirect(reverse("web:cart"))


@login_required(login_url=CUSTOMER_LOGIN_URL)
def add_address(request):

    if request.method == 'POST':
        form = CustomerAddressForm(request.POST)
        customer = Customer.objects.get(user=request.user,is_deleted=False)
        # if instance go to edit
        if form.is_valid() :
            data = form.save(commit=False)
            data.auto_id = get_auto_id(CustomerAddress)
            data.creator = request.user
            data.date_updated = datetime.today()
            data.updater = request.user
            data.customer = customer
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Address created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('web:create_order')
                }

        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = CustomerAddressForm()

        context = {
            'form': form,
            'page_name' : 'Create Address',
            'page_title' : 'Create Address',
            'url' : reverse('web:add_address'),
        }

        return render(request, 'web/address.html',context)


@login_required(login_url=CUSTOMER_LOGIN_URL)
def create_order(request):

    customer = Customer.objects.get(user=request.user,is_deleted=False)
    cart_instance =  CartItem.objects.filter(customer=customer,is_deleted=False)

    order_auto_id = get_auto_id(Order)
    count_len = len(str(order_auto_id))
    today = datetime.today()
    date_number = ""
    date_count = len(str(today.day))
    if date_count == 1:
        date_number = "0"+str(today.day)
    else :
            date_number = str(today.day)

    month_number = ""
    month_count = len(str(today.month))
    if month_count == 1:
        month_number = "0"+str(today.month)
    else :
        month_number = str(today.month)

    number = ""
    if count_len == 1:
        number = "000" + str(order_auto_id)
    elif count_len == 2:
        number = "00" + str(order_auto_id)
    elif count_len == 3:
        number = "0" + str(order_auto_id)
    else :
        number = str(order_auto_id)

    order_id = "OR" + str(today.year) + month_number + date_number + number

    total_amount = CartItem.objects.filter(customer__user=request.user,is_deleted=False).aggregate(total_price=Sum('unit_price'))["total_price"]

    if CustomerAddress.objects.filter(customer__user=request.user).exists():
        address = CustomerAddress.objects.filter(is_deleted=False).order_by('-id').first()

        order_data = Order.objects.create(
            auto_id = order_auto_id,
            creator = request.user,
            updater = request.user,

            order_id = order_id,
            time = datetime.today(),
            customer = customer,
            billing_address = address,
            total_amount = total_amount,
        )
        #message to customer

        for item in cart_instance:
            product = item.product
            qty = item.qty
            unit_price = item.unit_price

            OrderItem.objects.create(
                auto_id = get_auto_id(OrderItem),
                creator = request.user,
                updater = request.user,

                order = order_data,
                product = product,
                qty = qty,
                subtotal = unit_price,
            )
            # delete item from cart
            # CartItem.objects.filter(pk=item.pk).delete()

        Payment.objects.create(
            auto_id = get_auto_id(Payment),
            creator = request.user,
            updater = request.user,

            order_id = order_id,
            currency = "INR",
            description = "New Order",
            payment_mode = "LIVE",
            order_status = "Pending",
            amount = total_amount,
        )

        return redirect(reverse('web:payment_gateway',kwargs={'order_id':order_id}))
        # response_data = {
        #     "status" : "true",
        #     "message" : "Online Payment",
        #     'redirect' : 'true',
        #     "redirect_url": reverse('web:payment_gateway',kwargs={'order_id':order_id})
        # }

        # return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@csrf_protect
@csrf_exempt
def payment_gateway(request,order_id):
    if Payment.objects.filter(order_id=order_id,is_deleted=False).exists():
        payment_instance = Payment.objects.get(order_id=order_id,is_deleted=False)
        # print(payment_instance.amount)
        order_instance = Order.objects.get(order_id=order_id,is_deleted=False)
        order_currency = 'INR'
        order_receipt = order_id
        order_amount = payment_instance.amount
        name = order_instance.customer
        email = order_instance.customer.email
        notes = {'Shipping address': order_instance.billing_address.address}
        total_amount = order_amount * 100


        response = client.order.create(dict(amount=int(float(total_amount)), currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        payment_order_id =response['id']
        Payment.objects.filter(order_id=order_id,is_deleted=False).update(payment_order_id=payment_order_id)

    context = {
        "payment_order_id" : order_instance.order_id,
        "payment_order_id" : payment_order_id,
        "order_amount" : str(order_amount),
        "current_amount" : str(order_amount),
        "name" : name,
        "email" : email,
        "notes" : notes,
        "redirect_url": reverse('web:payment_response', kwargs={'order_id':order_id}),

        'page_name' : 'Payment Page',
        'page_title' : 'Payment Page',

    }

    return render(request, 'web/payment_page.html', context)

#=====================================payment section starting============================#
@csrf_protect
@csrf_exempt
@require_POST
def payment_response(request,order_id):
    # print("payment response")
    response = request.POST

    c = {}
    c.update(csrf(request))

    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }


    payment = Payment.objects.filter(payment_order_id=params_dict['razorpay_order_id'])
    # print(payment,"payment------------")
    order = Order.objects.get(order_id=order_id,is_deleted=False)
    # print(order,"------order----------")
    status = client.utility.verify_payment_signature(params_dict)
    # print(status,"status------------------------")
    if status == False:
        order.payment_status = "failed"
        order.save()

        return render(request, 'web/order_summary.html', {'status': 'Payment Faliure!!!'})
        return HttpResponseRedirect(reverse("web:payment_failed"))


    else:
        # print("else")
        payment.update(
            transaction_id = params_dict['razorpay_payment_id'],
            transaction_signature = params_dict['razorpay_signature'],
            amount = order.total_amount,
            order_status = "ordered",
            payment_datetime = datetime.now(),
        )


        if Customer.objects.filter(user=request.user,is_deleted=False).exists():
            customer = Customer.objects.get(user=request.user,is_deleted=False)
            # print(customer,"---------user------------")
            items = CartItem.objects.filter(customer__user=customer.user,is_deleted=False)
            # print(items,"------------items----------")
        order.payment_status = "received"
        order.save()

        if items:
            # print("inside items")
            for item in items :
                # print(item,"-------------------------ttrttrt")
                product = item.product

                #update stock
                product.stock-=item.qty
                product.save()


                if WhishlistItem.objects.filter(customer = customer,product=product).exists():
                    WhishlistItem.objects.filter(customer = customer,product=product).delete()

                # item.is_deleted = True
                # item.save()
                # delete item from cart
                CartItem.objects.filter(pk=item.pk,is_deleted=False).delete()

        success = "yes"
        message = "Success! Your transaction has been successfully processed."

        return HttpResponseRedirect(reverse("web:payment_success", kwargs={'order_id':order_id}))


def payments(request):
    title = "Payments"
    instances = Payment.objects.filter(is_deleted=False)
    success = request.GET.get('success')
    message = request.GET.get('message')

    query = request.GET.get("q")
    if query:
        instances = instances.filter(Q(amount__icontains=query) | Q(order_status__icontains=query) | Q(transaction_id__iexact=query) | Q(payment_order_id__iexact=query))
        title = "Payments - %s" %query

    context = {
        "instances" : instances,
        'title' : title,
        "success" : success,
        "message" : message,
        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_grid_system" : True,
        "is_need_animations" : True,
        "is_need_datetime_picker" : True,
    }
    return render(request,'web/payments/payments.html',context)



def payment(request,pk):
    instance = get_object_or_404(Payment.objects.filter(pk=pk,is_deleted=False))
    context = {
        "instance" : instance,
        "title" : "Payment : " + str(instance.amount),
        "single_page" : True,

        "is_need_select_picker" : True,
        "is_need_popup_box" : True,
        "is_need_custom_scroll_bar" : True,
        "is_need_wave_effect" : True,
        "is_need_bootstrap_growl" : True,
        "is_need_grid_system" : True,
        "is_need_animations" : True,
        "is_need_datetime_picker" : True,
    }
    return render(request,'web/payments/payment.html',context)



def payment_success(request,order_id):
    order =  Order.objects.get(order_id = order_id,is_deleted=False)
    items = OrderItem.objects.filter(order=order)

    context = {
        "order" : order,
        "order_items" : items,
        "title" : "Payment Success" ,
    }

    return render(request, 'web/payments/order-successfull.html', context)


def payment_failed(request):

    context = {
        "title" : "Payment Failed",
    }

    return render(request, 'web/payments/failure.html', context)

#===========================================payment section end================================#

def invoice(request,order_id):
    order =  Order.objects.get(order_id = order_id,is_deleted=False)
    items = OrderItem.objects.filter(order=order)

    context = {
        "order" : order,
        "order_items" : items,
        "title" : "Invoice",
    }

    return render(request, 'web/invoice.html', context)