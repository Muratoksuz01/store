from .models import *
import json
def cookiecart(request):
    try:
        cart=json.loads(request.COOKIES["cart"])
    except:
        cart={}
    print("data",cart)
    items=[]
    order={'get_cart_total':0,"get_cart_items":0}
    orderitem=order["get_cart_items"]
    for i in cart:
        try:
            orderitem=cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            item={
                'product' : 
                {
                    'id':product.id,
                    'name' : product.name,
                    'price' :product.price,
                    'imageURL' : product.imageURL
                },
                'quantity': cart[i]["quantity"] ,
                'get_total' : total
            }
            items.append(item)
            if product.digital==False:
                order["shipping"]=True
        except:
            pass
    return {"items":items,"order":order,"orderitem":orderitem}

def cartData(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        #customer, created = Customer.objects.get_or_create(user=request.user, email=request.user.email)
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        orderitem=order.get_cart_items

    else:
        cookieData=cookiecart(request)
        items=cookieData["items"]
        order=cookieData["order"]
        orderitem=cookieData["orderitem"]

    return {"items":items,"order":order,"orderitem":orderitem}

def guestOrder(request,data):
    name=data['form']["name"]
    email=data['form']["email"]
    cookieData=cookiecart(request)
    items=cookieData["items"]
    customer,created=Customer.objects.get_or_create(email=email)
    customer.name=name
    customer.save()
    order=Order.objects.create(customer=customer,complete=False)
    for item in items:
        product=Product.objects.get(id=item["id"])
        orderitem=OrderItem.objects.create(product=product,order=order,quantity=item["quantity"])
        return customer,order