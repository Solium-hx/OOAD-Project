import re
from django.contrib.auth.models import Group,User
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced,PickOrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm, ShopRegistrationForm

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
  def get(self,request):
     Topwears = Product.objects.filter(category='TW')
     Jeans = Product.objects.filter(category='J')
     Mobiles = Product.objects.filter(category='M')
     Laptop = Product.objects.filter(category='L')
     Covid_Medicines = Product.objects.filter(category='CM')
     Sanitizer = Product.objects.filter(category='S')
     Mask = Product.objects.filter(category='MK')
     Grocerys = Product.objects.filter(category='G')
     Kitchen_Essentials = Product.objects.filter(category='K')
     return render(request,'app/home.html',{'Topwears':Topwears,'Jeans':Jeans,'Mobiles':Mobiles,'Kitchen_Essentials':Kitchen_Essentials,'Grocerys':Grocerys,'Mask':Mask,'Sanitizer':Sanitizer,'Covid_Medicines':Covid_Medicines,'Laptop':Laptop})




#def product_detail(request):
 #return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart= False
        if request.user.is_authenticated:
                    item_already_in_cart= Cart.objects.filter(Q(product=product.id) &Q(user=request.user))
        return render(request,'app/productdetail.html',{'product':product ,'item_already_in_cart':item_already_in_cart})




@login_required()
def add_to_cart(request):
        user =request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')
@login_required()
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'cart':cart ,'totalamount':totalamount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')

@login_required()
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

@login_required()
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

@login_required()
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.delete()
        amount=0.0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data={
            'amount': amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
@login_required()
def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required()
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required()
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

@login_required()
def pick(request):
    op = PickOrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/pickup.html',{'pickorder_placed':op})

def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Samsung' or data =='Apple' or data =='Oppo' or data =='Redmi':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20001)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})



def Laptop(request,data=None):
    if data == None:
        Laptops = Product.objects.filter(category='L')
    elif data =='Lenovo' or data=='Apple' or data=='HP'  :
        Laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        Laptops = Product.objects.filter(category='L').filter(discounted_price__lt=60001)
    elif data == 'above':
        Laptops = Product.objects.filter(category='L').filter(discounted_price__gt=60000)
    return render(request, 'app/laptop.html',{'Laptops':Laptops})

def Jeans(request,data=None):
    if data == None:
        Jeans = Product.objects.filter(category='J')
    elif data =='Levis' or data=='VanHeusen' or data=='Mufti' :
        Jeans = Product.objects.filter(category='J').filter(brand=data)
    elif data == 'below':
        Jeans = Product.objects.filter(category='J').filter(discounted_price__lt=1201)
    elif data == 'above':
        Jeans = Product.objects.filter(category='J').filter(discounted_price__gt=1200)
    return render(request, 'app/Jeans.html',{'Jeans':Jeans})

def TopWear(request,data=None):
    if data == None:
        TopWears = Product.objects.filter(category='TW')
    elif data =='Levis' or data=='Nike' or data=='Mufti':
        TopWears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        TopWears = Product.objects.filter(category='TW').filter(discounted_price__lt=501)
    elif data == 'above':
        TopWears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)

    return render(request, 'app/TopWear.html',{'TopWears':TopWears})


def CovidMedicine(request):
     CovidMedicines = Product.objects.filter(category='CM')
    #elif data =='samsung' or data=='apple' or data=='oppo' or data=='redmi' :
     #   mobiles = Product.objects.filter(category='M').filter(brand=data)
     return render(request, 'app/CovidMedicine.html',{'CovidMedicines':CovidMedicines})


def Mask(request):
    Masks = Product.objects.filter(category='MK')
    # elif data =='samsung' or data=='apple' or data=='oppo' or data=='redmi' :
    #   mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/Mask.html', {'Masks': Masks})

def Sanitizer(request):
    Sanitizers = Product.objects.filter(category='S')
    # elif data =='samsung' or data=='apple' or data=='oppo' or data=='redmi' :
    #   mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/Sanitizer.html', {'Sanitizers': Sanitizers})

def KitchenEssential(request, data=None):
    if data == None:
        KitchenEssentials = Product.objects.filter(category='K')
    elif data == 'Sunflame' or data == 'Bajaj' or data == 'Usha' or data == 'Prestige':
        KitchenEssentials = Product.objects.filter(category='K').filter(brand=data)
    elif data == 'below':
        KitchenEssentials = Product.objects.filter(category='K').filter(discounted_price__lt=1801)
    elif data == 'above':
        KitchenEssentials = Product.objects.filter(category='K').filter(discounted_price__gt=1800)

    return render(request, 'app/KitchenEssential.html', {'KitchenEssentials': KitchenEssentials})

def Grocery(request, data=None):
    if data == None:
        Grocerys = Product.objects.filter(category='G')
    elif data == 'Fruits' or data == 'Vegetables' or data == 'Complan' or data == 'Amul' or data == 'Haldirams':
        Grocerys = Product.objects.filter(category='G').filter(brand=data)
    return render(request, 'app/Grocery.html', {'Grocerys': Grocerys})

def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        tle = Product.objects.all().filter(title__icontains=search)
        cat = Product.objects.all().filter(category__icontains=search)
        bnd = Product.objects.all().filter(brand__icontains=search)
        desc = Product.objects.all().filter(description__icontains=search)
        pin = Product.objects.all().filter(pincode_of_shop=search)
        add = Product.objects.all().filter(address__icontains=search)
        post=tle|cat|bnd|desc|pin|add
        return render(request,'app/searchbar.html',{'post':post})

class ShopRegistrationView(View):

    def get(self,request):
        form =ShopRegistrationForm()
        return render(request, 'app/shopregistration.html',{'form':form})


    def post(self,request):
        form=ShopRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! You are registered Successfully!')
            user=form.save()
            group = Group.objects.get(name='ShopOwner')
            user.groups.add(group)
        return render(request,'app/shopregistration.html',{'form':form})


class CustomerRegistrationView(View):

    def get(self,request):
        form =CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})


    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! You are registered Successfully!')
            user = form.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
        return render(request,'app/customerregistration.html',{'form':form})


@login_required()
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

@login_required()
def checkout2(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout2.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


@login_required()
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@login_required()
def pickpayment_done(request):
    user = request.user
    custid1 = request.GET.get('custid')
    customer1 = Customer.objects.get(id=custid1)
    cart1 = Cart.objects.filter(user=user)
    for c in cart1:
        PickOrderPlaced(user=user, customer=customer1, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("pick")

@method_decorator(login_required(), name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html' , {'form':form,'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            Pincode = form.cleaned_data['Pincode']
            reg = Customer(user=usr,name=name, locality=locality, city=city,  Pincode=Pincode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
            return render(request, 'app/profile.html', {'form':form,'active':'btn-primary'})








