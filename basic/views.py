from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Ouds, Review, Order, QuantityManagement, Tracker, Categories, ContactUs, UserOrder, Promos, WebContents, Moderators, ShippingAddress, Analytics
import os


CLIENT_ID = '31889031476-0dhc7cpg32shmjhv7megtv0do7ndp1q2.apps.googleusercontent.com'

def index(request):
    ouds = Ouds.objects.all().order_by("-id")
    paginator = Paginator(ouds, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "basic/index.html",{
        "ouds" : page_obj,
    })

def home(request):
    category = Categories.objects.get(name="Exclusive")
    ouds = Ouds.objects.filter(category=category)
    return render(request, "basic/home.html",{
        "ouds" : ouds,
    })


def exclusive(request):
    category = Categories.objects.get(name="Exclusive")
    ouds = Ouds.objects.filter(category=category)
    return render(request, "basic/exclusive.html",{
        "ouds" : ouds,
    })

def category(request, category_name):
    category = Categories.objects.get(name=category_name)
    try:
        ouds = Ouds.objects.filter(category=category).order_by("-id")
    except:
        return render(request, "basic/error.html")
    
    return render(request, "basic/category.html", {
        "ouds" :ouds,
        "category" : category,
    })




# user login option
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = authenticate(request, username=username, password=password)
        
        else:
            return render(request, "basic/login.html", {
                "message": "Username and password, both are required."
            })

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "basic/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "basic/login.html")


#user logout 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


#user register 
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        img = request.FILES.get('profile_pic', None)
        cover = request.FILES.get('cover_pic', None)
        bio = request.POST["bio"]
        if password != confirmation:
            return render(request, "basic/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            if img:
                user.img = img
            if bio:
                user.bios = bio
            if cover:
                user.cover = cover
            user.save()
        except IntegrityError:
            return render(request, "basic/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "basic/register.html")



def update_amount(request, oud_id):
    oud = Ouds.objects.get(pk=oud_id)
    return JsonResponse(oud.serialize())


def oud_page(request, oud_id):
    oud = Ouds.objects.get(pk=oud_id)
    ouds = Ouds.objects.filter(category=oud.category)
    review = None
    if Review.objects.filter(oud=oud):
        review = Review.objects.filter(oud=oud)
    return render(request, "basic/oud_page.html",{
        "oud" : oud,
        "reviews" : review,
        "ouds" : ouds,
    })


def review(request, oud_id):
    oud = Ouds.objects.get(pk=oud_id)
    review = request.POST.get('review')
    review = Review(user = request.user, oud = oud, review = review)
    review.save()
    return HttpResponseRedirect(reverse("oud_page", args=(oud.id,)))


def show_cart(request):
    id = None
    return render(request, "basic/cart.html",{
        'id' : id,
        'validation' : False,
    })

def take_order(request):
    if request.method == 'POST':
        name = request.POST.get("name", '')
        email = request.POST.get("email", '')
        total_price = request.POST.get("total_price", 0.00)
        delivery_charge = request.POST.get("delivery_charge", 0.00)
        promo_discount = request.POST.get("promo_discount", 0.00)
        address = request.POST.get("address", '')
        area = request.POST.get("area", '')
        town=request.POST.get("town", '')
        city = request.POST.get("city", '')
        country = request.POST.get("country", '')
        phone = request.POST.get("phone", '')
        zip = request.POST.get("zip", '')
        orders = request.POST.get("itemsJSON", '')
        if len(orders) < 8:
            return render(request, "basic/error.html")
        order = Order(name=name, email=email, address=address, city=city, country=country, phone=phone, zip=zip, order=orders, total_price=total_price, area = area, town=town, promo_discount = promo_discount, delivery_charge=delivery_charge)
        order.save()
        tracker = Tracker(order=order, email=email, desc="Order has been placed and you will shortly notified of your product delivery date.")
        tracker.save()

        user_order = UserOrder(order = order, user = request.user)
        user_order.save()

        return render(request, "basic/cart.html", {
            'validation' : True,
            'id' : order.id,
        })
    return render(request, "basic/cart.html", {
        'validation' : False,
        'id' : id,
    })


def show_tracker(request):
    if request.method == 'POST':
        try:
            email = request.POST.get("email", "")
            id = request.POST.get("id", "")
            user = User.objects.filter(email=email)
            order = Order.objects.get(pk=id)
            tracker = Tracker.objects.get(order=order, email=email)
            test = json.loads(order.order)
            amount = order.total_price
            return render(request, "basic/tracker.html",{
                "tracker" : tracker,
                "order" : order,
                "item_list" : test,
                "total_price" : amount,
            })

        except:
            return render(request, "basic/tracker.html",{
                "message" : "Please fill up the from with valid information",
            })
    return render(request, "basic/tracker.html")


def search(request):
    query = request.GET.get("search", "")
    search_result = []
    category_list = []
    products = Ouds.objects.all()
    for product in products:
        if query in product.description:
            search_result.append(product)
            category_list.append(product.category.name)
    
    search_result = reversed(search_result)
    return render(request, "basic/search.html", {
        "ouds" : search_result,
        "category_list" : category_list,
    })


def contact_us(request):
    msg = None
    if request.method == "POST":
        
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        phoneno = request.POST.get("phoneno", "")
        message = request.POST.get("message", "")
        if message != "" and email != "" and name != "" and phoneno != "":
            contact_us = ContactUs(name=name, email=email, phoneno=phoneno, message=message)
            contact_us.save()
            return render(request, "basic/contact_us.html", {
                "message" : "Thank You for contacting us. Someone from our team will contact you soon.",
            })
        else:
            return render(request, "basic/contact_us.html",{
                "message" : "Please fill up the from with valid information",
            })

        """
        except:
            return render(request, "basic/contact_us.html",{
                "message" : "Please fill up the from with valid information",
            })
        """

        
    return render(request, "basic/contact_us.html",{
        "message" : msg,
    })



def test_slider(request):
    return render(request, "basic/slider.html")
        
@login_required(login_url='login')
def admin_page(request):
    user_data = User.objects.all()
    oud_data = Ouds.objects.all()
    promo_data = Promos.objects.all()
    quantity_data = QuantityManagement.objects.all()
    review_data = Review.objects.all()
    order_data = Order.objects.all()
    tracker_data = Tracker.objects.all()
    web_data = WebContents.objects.get(pk=1)
    contact_us = ContactUs.objects.all()
    moderators = Moderators.objects.all()
    category_data = Categories.objects.all()

    return render(request, "basic/admin_page.html", {
        "user_data" : user_data,
        "ouds" : oud_data.order_by("-id"),
        "promos" : promo_data,
        "quantity_data" : quantity_data,
        "reviews": review_data,
        "orders" : order_data.order_by("-id"),
        "trackers" : tracker_data.order_by("-id"),
        "contents" : web_data,
        "contactus_data" : contact_us,
        "moderators" : moderators,
        "categories" : category_data, 
    })


@login_required(login_url='login')
def profile_page(request):
    user = request.user
    user_order_link = None
    shipping_address = None
    if UserOrder.objects.filter(user = user):
        user_orders_link = UserOrder.objects.filter(user = user)

    if ShippingAddress.objects.filter(user = user):
        shipping_address = ShippingAddress.objects.filter(user = user)
    return render(request, "basic/profile_page.html",{
        "user_order_data" : user_orders_link,
        "shipping_addresses" : shipping_address,
    })

@login_required(login_url='login')
def individual_user_page(request, user_id):
    user = User.objects.get(pk = user_id)
    shipping_address = None
    user_orders = None
    if ShippingAddress.objects.filter(user = user):
        shipping_address = ShippingAddress.objects.filter(user = user)

    if UserOrder.objects.filter(user = user):
        user_orders = UserOrder.objects.filter(user = user)
    
    return render(request, "basic/show_user.html", {
        "user_orders" : user_orders,
        "shipping_addresses" : shipping_address,
    })


@login_required(login_url='login')
def edit_ouds(request, oud_id):
    oud = Ouds.objects.get(pk = int(oud_id))
    quantity_list = QuantityManagement.objects.all()
    categories = Categories.objects.all()
    if request.method == "POST":
        title = request.POST.get("title", "")
        oud.title = title

        type = request.POST.get("type", "")
        oud.type = type

        description = request.POST.get("description", "")
        oud.description = description

        exerpt = request.POST.get("exerpt", '')
        oud.exerpt = exerpt

        base_price = request.POST.get("base_price", '')
        oud.base_price = float(base_price)

        amount = request.POST.get("amount", "")
        oud.amount = float(amount)

        base_amount = request.POST.get("base_amount", "")
        oud.base_amount = base_amount

        price_1 = request.POST.get("price_1", "")
        oud.price_1 = float(price_1)

        price_2 = request.POST.get("price_2", "")
        oud.price_2 = float(price_2)

        price_3 = request.POST.get("price_3", "")
        oud.price_3 = float(price_3)

        price_4 = request.POST.get("price_4", "")
        oud.price_4 = float(price_4)

        prev_price_1 = request.POST.get("prev_price_1", "")
        oud.prev_price_1 = float(prev_price_1)

        prev_price_2 = request.POST.get("prev_price_2", "")
        oud.prev_price_2 = float(prev_price_2)

        prev_price_3 = request.POST.get("prev_price_3", "")
        oud.prev_price_3 = float(prev_price_3)

        prev_price_4 = request.POST.get("prev_price_4", "")
        oud.prev_price_4 = float(prev_price_4)

        offer_status = request.POST.get("offer_status", "")
        oud.offer_status = offer_status

        offer_amount = request.POST.get("offer_amount", "")
        oud.offer_amount = int(offer_amount)

        img = request.FILES.get('img', None)
        if img:
            oud.img = img

        cover_image1 = request.FILES.get('cover_image1', None)
        if cover_image1:
            oud.cover_image1 = cover_image1

        amount_type = request.POST.getlist("amount_type")
        oud.amount_type.clear()
        print(amount_type)
        
        for amount in amount_type:
            quantity = QuantityManagement.objects.get(amount=amount)
            oud.amount_type.add(quantity)

        print(oud.amount_type)
        print("print anything")

        amount_number = request.POST.get("amount_number", "")
        oud.amount_number = int(amount_number)

        category = request.POST.get("category", "")
        category = Categories.objects.get(name=category)
        oud.category = category

        tags = request.POST.get("tags", '')
        oud.tags = tags

        oud.save()
        return HttpResponseRedirect(reverse("admin_page"))

    return render(request, "basic/oud_edit.html", {
        "oud" : oud,
        "quantity_list" : quantity_list,
        "categories" : categories,
    })


def add_oud(request):
    quantity_list = QuantityManagement.objects.all()
    categories = Categories.objects.all()
    if request.method == "POST":
        title = request.POST.get("title", "")
        
        type = request.POST.get("type", "")
        
        description = request.POST.get("description", "")
        
        exerpt = request.POST.get("exerpt", '')
        
        base_price = request.POST.get("base_price", '')
        
        amount = float(request.POST.get("amount", 0.00))
        
        base_amount = float(request.POST.get("base_amount", 0.00))
        
        price_1 = request.POST.get("price_1", "")
        
        price_2 = request.POST.get("price_2", "")
        
        price_3 = request.POST.get("price_3", "")
        
        price_4 = request.POST.get("price_4", "")
        
        prev_price_1 = request.POST.get("prev_price_1", "")
        
        prev_price_2 = request.POST.get("prev_price_2", "")

        prev_price_3 = request.POST.get("prev_price_3", "")
        
        prev_price_4 = request.POST.get("prev_price_4", "")

        offer_status = request.POST.get("offer_status", "")

        offer_amount = request.POST.get("offer_amount", "")
        
        amount_type = request.POST.getlist("amount_type")
        
        amount_number = int(request.POST.get("amount_number", ""))
        
        category = request.POST.get("category", "")

        category = Categories.objects.get(name=category)
       
        tags = request.POST.get("tags", '')
        
        oud = Ouds.objects.create(title = title, type=type, description=description, exerpt=exerpt, amount=amount, base_price=base_price,base_amount=base_amount, price_1=price_1, price_2= price_2, price_3=price_3, price_4= price_4, prev_price_1= prev_price_1, prev_price_2=prev_price_2, prev_price_3=prev_price_3, prev_price_4=prev_price_4, offer_status=offer_status, offer_amount=offer_amount, category=category, amount_number=amount_number, tags=tags)

        img = request.FILES.get('img', None)
        if img:
            oud.img = img

        cover_image1 = request.FILES.get('cover_image1', None)
        if cover_image1:
            oud.cover_image1 = cover_image1

        for amount in amount_type:
            quantity = QuantityManagement.objects.get(amount=amount)
            oud.amount_type.add(quantity)

        oud.save()
        return HttpResponseRedirect(reverse("admin_page"))
    return render(request, "basic/oud_add.html", {
        "quantity_list" : quantity_list,
        "categories" : categories,
    })
    

@login_required(login_url='login')
def show_order(request, order_id):
    order = Order.objects.get(pk = order_id)
    order_data = order.order
    order_dict = json.loads(order_data)
    order_tracker = Tracker.objects.get(order=order)
    for ordr in order_dict:
        amount = order_dict[ordr][3]
        amount_arr = order_dict[ordr][5]
        price_arr = order_dict[ordr][7]
        
        for i in range(len(amount_arr)):
            if float(amount) == float(amount_arr[i]):
                order_dict[ordr].append(float(price_arr[i]) * int(order_dict[ordr][0]))
                
        
            
            

    user = None
    if UserOrder.objects.filter(order = order):
        user_order_data = UserOrder.objects.get(order = order)
        user = user_order_data.user

    product_price = order.total_price + order.promo_discount - order.delivery_charge
        
   
    return render(request, "basic/order.html",{
        "orders" : order_dict,
        "main_order" : order,
        "user_of_order" : user,
        "product_price" : product_price,
        "tracker" : order_tracker,
    })
    

def show_content(request):
    web_contents = WebContents.objects.get(pk = 1)
    return JsonResponse(web_contents.serialize())

@login_required(login_url='login')
def change_content(request):
    web_contents = WebContents.objects.get(pk = 1)
    if request.method == 'POST':
        print("comes here")
        aboutus = request.POST.get("aboutus", "")
        web_contents.aboutus = aboutus

        privacy_policy = request.POST.get("privacy_policy", "")
        web_contents.privacy_policy = privacy_policy

        payment_policy = request.POST.get("payment_policy", "")
        web_contents.payment_policy = payment_policy

        shipping_policy = request.POST.get("shipping_policy", "")
        web_contents.shipping_policy = shipping_policy

        terms_and_conditions = request.POST.get("terms_and_conditions", "")
        web_contents.term_and_conditions = terms_and_conditions

        exchange_and_return = request.POST.get("exchange_and_return", "")
        web_contents.exchange_and_return = exchange_and_return

        delivery_charge = request.POST.get("delivery_charge", "")
        web_contents.delivery_charge = int(delivery_charge)

        contact_no = request.POST.get("contact_no", "")
        web_contents.contact_no = contact_no

        contact_no_2 = request.POST.get("contact_no_2", "")
        web_contents.contact_no_2 = contact_no_2

        email = request.POST.get("email", "")
        web_contents.email = email

        featured_product_1 = request.POST.get("featured_1", "")
        web_contents.featured_product_id_1 = featured_product_1

        featured_product_2 = request.POST.get("featured_2", "")
        web_contents.featured_product_id_2 = featured_product_2

        featured_product_3 = request.POST.get("featured_3", "")
        web_contents.featured_product_id_3 = featured_product_3

        web_contents.save()

        return HttpResponseRedirect(reverse("admin_page"))
    
    return render(request, "basic/change_content.html", {
        "web_content" : web_contents,
    })



@login_required(login_url='login')
def check_promo(request, promo_code):
    promo = None
    try:
        promo = Promos.objects.get(name=promo_code)
    except Promos.DoesNotExist:
        promo = Promos.objects.get(id=3)
    
    return JsonResponse(promo.serialize())


@login_required(login_url='login')
def change_visibility(request, oud_id):
    oud = Ouds.objects.get(pk = oud_id)

    if oud.visibility:
        oud.visibility = False
    else:
        oud.visibility = True
    oud.save()
    return JsonResponse(oud.serialize())



@login_required(login_url='login')
@csrf_exempt
def delete_record(request, what, nice_id):
    record = None
    if what == "product":
        record = Ouds.objects.get(pk = nice_id)

    elif what == "review":
        record = Review.objects.get(pk = nice_id)
        
    elif what == "quantity":
        record = QuantityManagement.objects.get(pk = nice_id)

    elif what == "shipping":
        record = ShippingAddress.objects.get(pk = nice_id)
        
    elif what == "moderator":
        record = Moderators.objects.get(pk = nice_id)
        
    elif what == "order":
        record = Order.objects.get(pk = nice_id)
        
    elif what == "category":
        record = Categories.objects.get(pk = nice_id)
        
    elif what == "promo":
        record = Promos.objects.get(pk = nice_id)
        
    elif what == "contact":
        record = ContactUs.objects.get(pk = nice_id)

    elif what == "tracker":
        record = Tracker.objects.get(pk = nice_id)
        
    elif what == "user":
        record = User.objects.get(pk=nice_id)
    
    record.delete()

    return HttpResponseRedirect(reverse("admin_page"))


def show_aboutus(request):
    web_contents = WebContents.objects.get(pk=1)
    return render(request, "basic/about_us.html", {
        "web_contents" : web_contents,
    })



def add_category(request):
    if request.method == 'POST':
        name = request.POST.get("name", "")
        category = Categories.objects.create(name = name)
        category.save()
        
    return HttpResponseRedirect(reverse("admin_page"))



def add_promo(request):
    
    if request.method == 'POST':
        
        name = request.POST.get("name", "")
        
        discount_amount = request.POST.get("discount_amount", "")
        
        promo = Promos.objects.create(name = name, discount_amount=discount_amount)
        promo.save()
        
    return HttpResponseRedirect(reverse("admin_page"))
        

def add_quantity(request):
    
    if request.method == 'POST':
        amount = request.POST.get("amount", "")
        quantity = QuantityManagement.objects.create(amount = amount)
        quantity.save()

    return HttpResponseRedirect(reverse("admin_page"))


@csrf_exempt
def edit_record(request, what, nice_id):
    record = None


    if what == "review":
        record = Review.objects.get(pk = nice_id)
        
    elif what == "quantity":
        record = QuantityManagement.objects.get(pk = nice_id)
        data = json.loads(request.body)
        amount = data.get("val", "")
        record.amount = float(amount)
        record.save()

    elif what == "shipping":
        record = ShippingAddress.objects.get(pk = nice_id)
        
    elif what == "moderator":
        record = Moderators.objects.get(pk = nice_id)
        
    elif what == "order":
        record = Order.objects.get(pk = nice_id)
        
        
    elif what == "category":
        record = Categories.objects.get(pk = nice_id)
        data = json.loads(request.body)
        name = data.get("val", "")
        record.name = name
        record.save()

        
    elif what == "promo":
        record = Promos.objects.get(pk = nice_id)
        data = json.loads(request.body)
        name = data.get("val", "")
        discount_amount = data.get("")
        record.name = name
        record.save()
    
    return JsonResponse(record.serialize())
        

    
def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id)

    order.status = "Cancelled"
    order.save()

    return JsonResponse(order.serialize())


def show_profile_page(request, user_id):
    user = User.objects.get(pk=user_id)
    order = None
    if UserOrder.objects.filter(user = user):
        order = UserOrder.objects.filter(user = user)
    
    shipping_address = None

    if ShippingAddress.objects.filter(user = user):
        shipping_address = ShippingAddress.objects.filter(user= user)

    wishlist = None


    return render(request, "basic/profile_page.html", {
        "user_data" : user,
        "orders" : order,
        "shipping_addresses" : shipping_address,
        "wishlist" : wishlist, 
    })


def add_shipping(request):
    user = request.user
    if request.method == 'POST':
        pass

    return HttpResponseRedirect(reverse("profile_page", args=(user.id,)))

    
def change_profile(request, user_id):
    user = User.objects.get(pk = user_id)

    if request.method == 'POST':
        user.username = request.POST.get("username", "")
        user.email = request.POST.get("email", "")
        user.full_name = request.POST.get("fullname", "")
        user.gender = request.POST.get("gender", "")
        user.contact_no = request.POST.get("contact_no", "")
        user.save()

    return HttpResponseRedirect(reverse("profile_page", args=(user.id,)))

