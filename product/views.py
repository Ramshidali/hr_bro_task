#standerd
import json
import datetime
#django
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
#thirdparty
#local
from product.forms import *
from main.functions import generate_form_errors, get_auto_id, paginate
from product.models import *
from main.decorators import role_required


# #*******************************CRUD Brands***************************************


@login_required
@role_required(['superadmin'])
def brands(request):
    """
    brands listings
    :param request:
    :return: brands list view
    """
    instances = Brand.objects.filter(is_deleted=False).order_by("-id")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query)
        )
        title = "Brands - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Brands',
        'page_title' : 'Brands',
        'filter_data' :filter_data,
    }

    return render(request, 'admin_panel/product/brand.html', context)


@login_required
@role_required(['superadmin'])
def create_brand(request):
    """
    create operation of brand
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        # if instance go to edit
        form = BrandsForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Brand)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "brand created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:brand')
            }

        else:
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = BrandsForm()

        context = {
            'form': form,
            'page_name' : 'Create brand',
            'page_title' : 'Create brand',
            'url' : reverse('product:create_brand'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_brand(request,pk):
    """
    edit operation of brand
    :param request:
    :param pk:
    :return:
    """
    instance = get_object_or_404(Brand, pk=pk)

    message = ''
    if request.method == 'POST':
        form = BrandsForm(request.POST,instance=instance)

        if form.is_valid():

            #update brand
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "brand Update successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:brand')
            }

        else:
            message = generate_form_errors(form ,formset=False)


            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = BrandsForm(instance=instance)

        context = {
            'form': form,
            'page_name' : 'Create brand',
            'page_title' : 'Create brand',
            'is_need_select2' : True,
            'url' : reverse('product:brand'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def delete_brand(request, pk):
    """
    brand deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Brand.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:brand')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


#*******************************CRUD Product***************************************


@login_required
@role_required(['superadmin'])
def product_list(request):
    """
    product listings
    :param request:
    :return: product list view
    """
    instances = Product.objects.filter(is_deleted=False).order_by("-date_added")

    filter_data = {}
    query = request.GET.get("q")

    if query:

        instances = instances.filter(
            Q(auto_id__icontains=query) |
            Q(name__icontains=query) |
            Q(brand__name__icontains=query)
        )
        title = "Products - %s" % query
        filter_data['q'] = query


    context = {
        'instances': instances,
        'page_name' : 'Products',
        'page_title' : 'Products',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/product/product_list.html', context)


@login_required
@role_required(['superadmin'])
def product_details(request,pk):
    """
    product single view using product pk
    :param request:
    :pk
    :return: product list view
    """
    instance = Product.objects.get(pk=pk, is_deleted=False)

    context = {
        'instance': instance,
        'page_name' : 'Product Details',
        'page_title' : 'Product Details',
        'is_need_light_box' : True,
    }

    return render(request, 'admin_panel/product/product_details.html', context)


@login_required
@role_required(['superadmin'])
def create_product(request):
    """
    create operation of product
    :param request:
    :return:
    """

    message = ''
    if request.method == 'POST':
        form = ProductForm(request.POST,files=request.FILES)

        if form.is_valid() :

            #create product
            data = form.save(commit=False)
            data.auto_id = get_auto_id(Product)
            data.creator = request.user
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Product created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('product:product_list')
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
        form = ProductForm()

        context = {
            'form': form,
            'page_name' : 'Create Product',
            'page_title' : 'Create Product',
            'is_need_select2' : True,
            'url' : reverse('product:create_product'),
        }

        return render(request, 'admin_panel/create/create.html',context)


@login_required
@role_required(['superadmin'])
def edit_product(request,pk):
    """
    edit operation of product
    :param request:
    :param pk:
    :return:
    """
    product_instance = get_object_or_404(Product, pk=pk)

    message = ''

    if request.method == 'POST':
        form = ProductForm(request.POST,files=request.FILES,instance=product_instance)

        if form.is_valid():
            #create product
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Product Successfully Updated.",
                "redirect": "true",
                "redirect_url": reverse('product:product_list')
            }

        else:
            message = generate_form_errors(form,formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:

        form = ProductForm(instance=product_instance)

        context = {
            'form': form,
            'message': message,
            'page_name' : 'edit product'

        }

        return render(request, 'admin_panel/create/create.html', context)


@login_required
@role_required(['superadmin'])
def delete_product(request, pk):
    """
    product deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Product.objects.filter(pk=pk).update(is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('product:product_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')