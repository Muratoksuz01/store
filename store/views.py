import json,os
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import datetime
from. utils import cookiecart,cartData, guestOrder
# Create your views here
def store (request):
    data=cartData(request)
    order=data["order"]
    orderitem=data["orderitem"]
    products=Product.objects.all()
    context = {"products":products,"orderitem":orderitem,"order":order,"shipping":False}
    return render (request, 'store/store.html', context)
def cart (request):
    data=cartData(request)
    items=data["items"]
    order=data["order"]
    orderitem=data["orderitem"]     
    context = {"items":items,"order":order,"orderitem":orderitem,"shipping":False}
    return render (request, 'store/cart.html', context)
def checkout (request):
    data=cartData(request)
    items=data["items"]
    order=data["order"]
    orderitem=data["orderitem"]
    context = {"items":items,"order":order,"orderitem":orderitem,"shipping":'False'}
    return render (request, 'store/checkout.html', context)  




def updateItem(request):
    print("data",request.body)

    data = json.loads (request.body)
    productId = data['productid']
    action = data['action']
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderİtem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=="add":
        orderİtem.quantity=(orderİtem.quantity)+1
    if action=="remove":
        orderİtem.quantity=(orderİtem.quantity)-1
    orderİtem.save()
    if orderİtem.quantity<=0:
        orderİtem.delete()

def processorder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer,complete=False)
        
        
    else:
        customer,order=guestOrder(request,data)
    total=float(data["form"]["total"])
    order.transaction_id=transaction_id
    if total==float(order.get_cart_total):
        order.complete=True
    order.save()

    if order.shipping==True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"]

        )
    return JsonResponse("preosessed",safe=False)
