import vonage
from django.utils import timezone
import datetime
import random
import requests
from sslcommerz_lib import SSLCOMMERZ
import uuid
import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import User, Ouds, Review, Order, QuantityManagement, Tracker, Categories, ContactUs, UserOrder, Promos, WebContents, Moderators, ShippingAddress, Analytics, NoticeBoard
import os
import string
import secrets


CLIENT_ID = '31889031476-0dhc7cpg32shmjhv7megtv0do7ndp1q2.apps.googleusercontent.com'


def index(request):
    ouds = Ouds.objects.all().order_by("-id")
    paginator = Paginator(ouds, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    notices = NoticeBoard.objects.all()
    return render(request, "basic/index.html", {
        "ouds": page_obj,
        "noticeboard": notices,
    })


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password


def home(request):
    category = Categories.objects.get(name="Exclusive")
    ouds = Ouds.objects.filter(category=category)

    return render(request, "basic/home.html", {
        "ouds": ouds,

    })


def exclusive(request):
    category = Categories.objects.get(name="Exclusive")
    ouds = Ouds.objects.filter(category=category)
    return render(request, "basic/exclusive.html", {
        "ouds": ouds,
    })


def category(request, category_name):
    category = Categories.objects.get(name=category_name)
    try:
        ouds = Ouds.objects.filter(category=category).order_by("-id")
    except:
        return render(request, "basic/error.html")

    return render(request, "basic/category.html", {
        "ouds": ouds,
        "category": category,
    })


def send_OTP(contact, otp):

    client = vonage.Client(key="c7ffa548", secret="PYXCz6glC2fVwJm6")
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": contact,
            "text": f"Your OTP is {otp}",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(
            f"Message failed with error: {responseData['messages'][0]['error-text']}")


def change_password(request):
    if request.method == 'POST':
        contact_no = request.POST.get("contact_no", "")
        user = None
        print(contact_no)
        print("comes here")
        if User.objects.filter(contact=contact_no):
            user = User.objects.filter(contact=contact_no)[0]
        else:
            return render(request, "basic/password_change.html", {"message": "Contact number not found."})
        password = generate_random_password()
        user.set_password(password)
        print(user.username)
        print(password)
        user.save()
        message = f"Your username is {user.username} and Your new password is {password}. Please change it after login."
        send_OTP(contact_no, message)
        return render(request, "basic/password_change.html", {"message": "Your password has been changed. Please check your message for new password."})

    return render(request, "basic/password_change.html", {
        "message": "Please enter your contact number",
    })

# user login option


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            if user.contact_verified == False:
                request.session['contact'] = user.contact
                otp = random.randint(100000, 999999)
                send_OTP(user.contact, otp)
                return HttpResponseRedirect(reverse("verify_contact"))

            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "basic/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "basic/login.html")


# user logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def verify_contact(request):
    if request.method == "POST":
        contact = request.session.get('contact')
        if not contact:
            return render(request, "basic/contact_verification.html", {
                "message": "contact number not found. Please try again.",
                "contact": contact,
            })

        user = User.objects.get(contact=contact)
        otp = request.POST["otp"]

        if str(user.otp) != str(otp):
            return render(request, "basic/contact_verification.html", {
                "message": "Invalid OTP. Please Try again.",
                "contact": contact,
            })

        current_time = timezone.now()

        # expire the otp after 5 minutes
        if (current_time - user.otp_last_created).total_seconds() > 300:
            new_otp = random.randint(100000, 999999)
            user.otp = new_otp
            user.otp_last_created = datetime.datetime.now()
            user.save()

            print(new_otp)
            send_OTP(user.contact, "Your Otp is " + new_otp)

            return render(request, "basic/contact_verification.html", {
                "message": "OTP expired. Another OTP has been sent.",
                "contact": contact,
            })

        user.contact_verified = True
        user.otp = None
        user.save()

        request.session['contact'] = None
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "basic/contact_verification.html")


# user register

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        contact = request.POST["contact"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not email or not contact or not password or not confirmation:
            return render(request, "basic/register.html", {
                "message": "Please fill all the fields."
            })

        if password != confirmation:
            return render(request, "basic/register.html", {
                "message": "Passwords must match."
            })

        # OTP verification
        otp = random.randint(100000, 999999)
        contact_verified = False
        otp_last_created = datetime.datetime.now()

        print(otp)

        try:
            user = User.objects.create_user(
                username=username, email=email,  password=password, contact=contact, otp=otp, contact_verified=contact_verified, otp_last_created=otp_last_created)
        except IntegrityError:
            return render(request, "basic/register.html", {
                "message": "Username, email and contact must be unique."
            })
        request.session['contact'] = contact
        send_OTP(contact, "Your otp is " + otp)
        return HttpResponseRedirect(reverse("verify_contact"))
    else:
        return render(request, "basic/register.html")


def update_amount(request, oud_id):
    oud = Ouds.objects.get(pk=oud_id)
    return JsonResponse(oud.serialize())


def oud_page(request, oud_id):
    oud = Ouds.objects.get(pk=oud_id)
    ouds = Ouds.objects.filter(category=oud.category)
    notices = NoticeBoard.objects.all()
    review = None
    if Review.objects.filter(oud=oud):
        review = Review.objects.filter(oud=oud)
    return render(request, "basic/oud_page.html", {
        "oud": oud,
        "reviews": review,
        "ouds": ouds,
        "noticeboard": notices,
    })


def review(request, oud_id):
    oud = Ouds.objects.get(pk=oud_id)
    review = request.POST.get('review')
    review = Review(user=request.user, oud=oud, review=review)
    review.save()
    return HttpResponseRedirect(reverse("oud_page", args=(oud.id,)))


def show_cart(request):
    id = None
    return render(request, "basic/cart.html", {
        'id': id,
        'validation': False,
    })


@csrf_exempt
def payment_success(request):
    transaction_id = request.POST.get('tran_id')

    try:
        order = Order.objects.get(transaction_id=transaction_id)
    except Order.DoesNotExist:
        return HttpResponse("Order does not exist")

    # print(request.POST)
    val_id = request.POST.get('val_id')
    store_id = "ibnma6496853da64bf"
    store_passwd = "ibnma6496853da64bf@ssl"

    # Construct the validation API url
    url = f"https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php?val_id={val_id}&store_id={store_id}&store_passwd={store_passwd}&format=json"

    response = requests.get(url, verify=True)
    response_json = response.json()

    # print(response)
    # print(response_json)
    if response_json["status"] == "VALID":
        order.is_paid = True
        order.save()

        return render(request, "basic/payment_success.html",)

    return render(request, "basic/payment_failure.html",)


@csrf_exempt
def payment_failure(request):
    transaction_id = request.POST.get("tran_id")
    order = Order.objects.get(transaction_id=transaction_id)
    # print("deleted in failure")
    order.delete()

    return render(request, "basic/payment_failure.html",)


@csrf_exempt
def payment_cancel(request):
    transaction_id = request.POST.get("tran_id")
    order = Order.objects.get(transaction_id=transaction_id)
    print("deleted in cancel")
    # order.delete()

    return render(request, "basic/payment_cancel.html",)


def handle_online_payment(transaction_id):
    order = Order.objects.get(transaction_id=transaction_id)

    settings = {
        "store_id": "ibnma6496853da64bf",
        "store_pass": "ibnma6496853da64bf@ssl",
        "issandbox": True,
    }

    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body["total_amount"] = order.total_price
    post_body["currency"] = "BDT"
    post_body["tran_id"] = transaction_id
    post_body["success_url"] = "http://127.0.0.1:8000/payment/success/"
    post_body["fail_url"] = "http://127.0.0.1:8000/payment/failure/"
    post_body["cancel_url"] = "http://127.0.0.1:8000/payment/cancel/"
    post_body["emi_option"] = 0
    post_body["cus_name"] = order.name
    post_body["cus_email"] = order.email
    post_body["cus_phone"] = order.phone
    post_body["cus_add1"] = order.address
    post_body["cus_city"] = order.city
    post_body["cus_country"] = "Bangladesh"
    post_body["shipping_method"] = "NO"
    post_body["multi_card_name"] = ""
    post_body["num_of_item"] = 1
    post_body["product_name"] = "Perfume"
    post_body["product_category"] = "Perfume Category"
    post_body["product_profile"] = "general"

    return sslcz.createSession(post_body)


def take_order(request):
    if request.method == 'POST':
        name = request.POST.get("name", '')
        email = request.POST.get("email", '')
        total_price = request.POST.get("total_price", 0.00)
        delivery_charge = request.POST.get("delivery_charge", 0.00)
        promo_discount = request.POST.get("promo_discount", 0.00)
        payment_method = request.POST.get("payment_method", 'Cash')
        address = request.POST.get("address", '')

        city = request.POST.get("city", '')

        phone = request.POST.get("phone", '')
        zip = request.POST.get("zip", '')
        orders = request.POST.get("itemsJSON", '')
        if len(orders) < 8:
            return render(request, "basic/error.html")

        order = Order(name=name, email=email, address=address, city=city, phone=phone, zip=zip, order=orders, total_price=total_price,
                      promo_discount=promo_discount, delivery_charge=delivery_charge, payment_method=payment_method)
        order.save()

        if payment_method.lower() == 'online':
            transaction_id = uuid.uuid4().hex
            # making sure the transaction id is unique
            while Order.objects.filter(transaction_id=transaction_id):
                transaction_id = uuid.uuid4().hex

            order.is_paid = False
            order.transaction_id = transaction_id
            order.save()
            ssl_response = handle_online_payment(transaction_id)
            if not ssl_response["status"] == "SUCCESS":
                order.delete()

                # TODO: show proper error message in the template: payment gateway error.
                return render(request, "basic/cart.html", {
                    'message': "Payment gateway error. Please try again later.",
                    'validation': False,
                    'id': id,
                })

            tracker = Tracker(order=order, email=email,
                              desc="Order has been placed and you will shortly notified of your product delivery date.")
            tracker.save()

            user_order = UserOrder(
                order=order, user=request.user, order_date=datetime.date.today)
            user_order.save()

            return redirect(ssl_response["GatewayPageURL"])

        else:
            tracker = Tracker(order=order, email=email,
                              desc="Order has been placed and you will shortly notified of your product delivery date.")
            tracker.save()

            user_order = UserOrder(order=order, user=request.user)
            user_order.save()

            return show_order(request, order.id, "Done")

    return render(request, "basic/cart.html", {
        'validation': False,
        'id': id,
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
            return render(request, "basic/tracker.html", {
                "tracker": tracker,
                "order": order,
                "item_list": test,
                "total_price": amount,
            })

        except:
            return render(request, "basic/tracker.html", {
                "message": "Please fill up the from with valid information",
            })
    return render(request, "basic/tracker.html")


def show_trac(request, order_id):
    order = Order.objects.get(pk=order_id)
    tracker = Tracker.objects.get(order=order)
    progress = tracker.progress / 3 * 100
    return render(request, "basic/tracker_v2.html", {
        "tracker": tracker,
        "progress": progress,
    })


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
        "ouds": search_result,
        "category_list": category_list,
    })


def contact_us(request):
    msg = None
    if request.method == "POST":

        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        phoneno = request.POST.get("phoneno", "")
        message = request.POST.get("message", "")
        if message != "" and email != "" and name != "" and phoneno != "":
            contact_us = ContactUs(
                name=name, email=email, phoneno=phoneno, message=message)
            contact_us.save()
            return render(request, "basic/contact_us.html", {
                "message": "Thank You for contacting us. Someone from our team will contact you soon.",
            })
        else:
            return render(request, "basic/contact_us.html", {
                "message": "Please fill up the from with valid information",
            })

        """
        except:
            return render(request, "basic/contact_us.html",{
                "message" : "Please fill up the from with valid information",
            })
        """

    return render(request, "basic/contact_us.html", {
        "message": msg,
    })


def test_slider(request):
    return render(request, "basic/slider.html", {
        "ouds": Ouds.objects.all(),
    })


@login_required(login_url='login')
def admin_page(request):
    user_data = User.objects.all()
    oud_data = Ouds.objects.all()
    promo_data = Promos.objects.all()
    quantity_data = QuantityManagement.objects.all()
    review_data = Review.objects.all()
    order_data = UserOrder.objects.all()
    tracker_data = Tracker.objects.all()
    web_data = WebContents.objects.get(pk=1)
    contact_us = ContactUs.objects.all()
    moderators = Moderators.objects.all()
    category_data = Categories.objects.all()
    noticeboard = NoticeBoard.objects.all()

    return render(request, "basic/admin_page.html", {
        "user_data": user_data,
        "ouds": oud_data.order_by("-id"),
        "promos": promo_data,
        "quantity_data": quantity_data,
        "reviews": review_data,
        "orders": order_data.order_by("-id"),
        "trackers": tracker_data.order_by("-id"),
        "contents": web_data,
        "contactus_data": contact_us,
        "moderators": moderators,
        "categories": category_data,
        "noticeboard": noticeboard,
    })


@login_required(login_url='login')
def profile_page(request):
    user = request.user
    user_order_link = None
    shipping_address = None
    if UserOrder.objects.filter(user=user):
        user_orders_link = UserOrder.objects.filter(user=user)

    if ShippingAddress.objects.filter(user=user):
        shipping_address = ShippingAddress.objects.filter(user=user)
    return render(request, "basic/profile_page.html", {
        "user_order_data": user_orders_link,
        "shipping_addresses": shipping_address,
    })


@login_required(login_url='login')
def individual_user_page(request, user_id):
    user = User.objects.get(pk=user_id)
    shipping_address = None
    user_orders = None
    if ShippingAddress.objects.filter(user=user):
        shipping_address = ShippingAddress.objects.filter(user=user)

    if UserOrder.objects.filter(user=user):
        user_orders = UserOrder.objects.filter(user=user)

    return render(request, "basic/show_user.html", {
        "user_orders": user_orders,
        "shipping_addresses": shipping_address,
    })


@login_required(login_url='login')
def edit_ouds(request, oud_id):
    oud = Ouds.objects.get(pk=int(oud_id))
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

        cover_image2 = request.FILES.get('cover_image2', None)
        if cover_image2:
            oud.cover_image2 = cover_image2

        amount_type = request.POST.getlist("amount_type")
        oud.amount_type.clear()

        for amount in amount_type:
            quantity = QuantityManagement.objects.get(amount=amount)
            oud.amount_type.add(quantity)

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
        "oud": oud,
        "quantity_list": quantity_list,
        "categories": categories,
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

        oud = Ouds.objects.create(title=title, type=type, description=description, exerpt=exerpt, amount=amount, base_price=base_price, base_amount=base_amount, price_1=price_1, price_2=price_2, price_3=price_3, price_4=price_4,
                                  prev_price_1=prev_price_1, prev_price_2=prev_price_2, prev_price_3=prev_price_3, prev_price_4=prev_price_4, offer_status=offer_status, offer_amount=offer_amount, category=category, amount_number=amount_number, tags=tags)

        img = request.FILES.get('img', None)
        if img:
            oud.img = img

        cover_image1 = request.FILES.get('cover_image1', None)
        if cover_image1:
            oud.cover_image1 = cover_image1

        cover_image2 = request.FILES.get('cover_image2', None)
        if cover_image2:
            oud.cover_image2 = cover_image2

        for amount in amount_type:
            quantity = QuantityManagement.objects.get(amount=amount)
            oud.amount_type.add(quantity)

        oud.save()
        return HttpResponseRedirect(reverse("admin_page"))
    return render(request, "basic/oud_add.html", {
        "quantity_list": quantity_list,
        "categories": categories,
    })


@login_required(login_url='login')
def show_order(request, order_id, message=""):
    order = Order.objects.get(pk=order_id)
    order_data = order.order
    order_dict = json.loads(order_data)
    order_tracker = Tracker.objects.get(order=order)
    for ordr in order_dict:
        amount = order_dict[ordr][3]
        amount_arr = order_dict[ordr][5]
        price_arr = order_dict[ordr][7]

        for i in range(len(amount_arr)):
            if float(amount) == float(amount_arr[i]):
                order_dict[ordr].append(
                    float(price_arr[i]) * int(order_dict[ordr][0]))

    user = None
    if UserOrder.objects.filter(order=order):
        user_order_data = UserOrder.objects.get(order=order)
        user = user_order_data.user

    product_price = order.total_price + order.promo_discount - order.delivery_charge

    return render(request, "basic/order.html", {
        "orders": order_dict,
        "main_order": order,
        "user_of_order": user,
        "product_price": product_price,
        "tracker": order_tracker,
        "message": message,
    })


def show_content(request):
    web_contents = WebContents.objects.get(pk=1)
    return JsonResponse(web_contents.serialize())


@login_required(login_url='login')
def change_content(request):
    web_contents = WebContents.objects.get(pk=1)
    if request.method == 'POST':
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

        contact = request.POST.get("contact", "")
        web_contents.contact = contact

        contact_2 = request.POST.get("contact_2", "")
        web_contents.contact_2 = contact_2

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
        "web_content": web_contents,
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
    oud = Ouds.objects.get(pk=oud_id)

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
        record = Ouds.objects.get(pk=nice_id)

    elif what == "review":
        record = Review.objects.get(pk=nice_id)

    elif what == "quantity":
        record = QuantityManagement.objects.get(pk=nice_id)

    elif what == "shipping":
        record = ShippingAddress.objects.get(pk=nice_id)
        record.delete()
        return HttpResponseRedirect(reverse("profile_page", args=(request.user.id,)))

    elif what == "moderator":
        record = Moderators.objects.get(pk=nice_id)

    elif what == "order":
        record = Order.objects.get(pk=nice_id)

    elif what == "category":
        record = Categories.objects.get(pk=nice_id)

    elif what == "promo":
        record = Promos.objects.get(pk=nice_id)

    elif what == "contact":
        record = ContactUs.objects.get(pk=nice_id)

    elif what == "tracker":
        record = Tracker.objects.get(pk=nice_id)

    elif what == "user":
        record = User.objects.get(pk=nice_id)

    elif what == "notice":
        record = NoticeBoard.objects.get(pk=nice_id)

    record.delete()

    return HttpResponseRedirect(reverse("admin_page"))


def show_aboutus(request):
    web_contents = WebContents.objects.get(pk=1)
    return render(request, "basic/about_us.html", {
        "web_contents": web_contents,
    })


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get("name", "")
        category = Categories.objects.create(name=name)
        category.save()

    return HttpResponseRedirect(reverse("admin_page"))


def add_promo(request):

    if request.method == 'POST':

        name = request.POST.get("name", "")

        discount_amount = request.POST.get("discount_amount", "")

        promo = Promos.objects.create(
            name=name, discount_amount=discount_amount)
        promo.save()

    return HttpResponseRedirect(reverse("admin_page"))


def add_notice(request):
    if request.method == "POST":

        notice = request.POST.get("notice", "")
        notice = NoticeBoard(notice=notice)
        notice.save()
    return HttpResponseRedirect(reverse("admin_page"))


def add_quantity(request):

    if request.method == 'POST':
        amount = request.POST.get("amount", "")
        quantity = QuantityManagement.objects.create(amount=amount)
        quantity.save()

    return HttpResponseRedirect(reverse("admin_page"))


@csrf_exempt
def edit_record(request, what, nice_id):
    record = None

    if what == "review":
        record = Review.objects.get(pk=nice_id)

    elif what == "quantity":
        record = QuantityManagement.objects.get(pk=nice_id)
        data = json.loads(request.body)
        amount = data.get("val", "")
        record.amount = float(amount)

    elif what == "shipping":
        record = ShippingAddress.objects.get(pk=nice_id)
        record.name = request.POST.get("name", "")
        record.email = request.POST.get("email", "")
        record.phone = request.POST.get("contact", "")
        record.address = request.POST.get("address", "")
        record.city = request.POST.get("city", "")
        record.zip = request.POST.get("zip", "")

    elif what == "moderator":
        record = Moderators.objects.get(pk=nice_id)

    elif what == "order":
        record = Order.objects.get(pk=nice_id)

    elif what == "category":
        record = Categories.objects.get(pk=nice_id)
        data = json.loads(request.body)
        name = data.get("val", "")
        record.name = name

    elif what == "promo":
        record = Promos.objects.get(pk=nice_id)
        data = json.loads(request.body)
        name = data.get("val", "")
        discount_amount = data.get("")
        record.name = name

    elif what == "notice":
        record = NoticeBoard.objects.get(pk=nice_id)
        data = json.loads(request.body)
        notice = data.get("val", "")
        record.notice = notice

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
    if UserOrder.objects.filter(user=user):
        order = UserOrder.objects.filter(user=user).order_by("-id")

    shipping_address = None

    if ShippingAddress.objects.filter(user=user):
        shipping_address = ShippingAddress.objects.filter(user=user)

    wishlist = None

    return render(request, "basic/profile_page.html", {
        "user_data": user,
        "orders": order,
        "shipping_addresses": shipping_address,
        "wishlist": wishlist,
    })


def add_shipping(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        contact = request.POST.get("contact", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        zip = request.POST.get("zip", "")

        shipping_address = ShippingAddress(
            user=user, name=name, address=address, phone=contact, email=email, city=city, zip=zip)
        shipping_address.save()

        user.has_shipping = True
        user.default_shipping_id = shipping_address.id

        user.save()
        return HttpResponseRedirect(reverse("profile_page", args=(user.id,)))

    return HttpResponseRedirect(reverse("profile_page", args=(user.id,)))


def change_profile(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        user.username = request.POST.get("username", "")
        user.email = request.POST.get("email", "")
        user.full_name = request.POST.get("fullname", "")
        user.gender = request.POST.get("gender", "")
        user.contact = request.POST.get("contact", "")
        user.save()

    return HttpResponseRedirect(reverse("profile_page", args=(user.id,)))


def edit_shipping(request, user_id, what, nice_id):
    record = ShippingAddress.objects.get(pk=nice_id)
    record.name = request.POST.get("name", "")
    record.email = request.POST.get("email", "")
    record.phone = request.POST.get("contact_no", "")
    record.address = request.POST.get("address", "")
    record.city = request.POST.get("city", "")
    record.zip = request.POST.get("zip", "")
    record.save()
    return HttpResponseRedirect(reverse("profile_page", args=(user_id,)))


@csrf_exempt
def change_trac_value(request, value, order_id):
    if request.user.status == "user":
        return HttpResponseRedirect(reverse("show_tracker_user", args=(order_id,)))

    order = Order.objects.get(pk=order_id)
    order.status = "not delivered"
    tracker = Tracker.objects.get(order=order)
    tracker.progress = int(value)
    if int(value) == 3:
        order.status = "delivered"

    tracker.save()
    order.save()

    progress = tracker.progress / 3 * 100
    return JsonResponse({"value": value, "progress": progress})


def change_delivery_date(request, order_id):
    order = Order.objects.get(pk=order_id)
    tracker = Tracker.objects.get(order=order)
    var = request.POST.get("delivery_date", datetime.date.today)

    tracker.delivary_date = var
    tracker.save()
    return HttpResponseRedirect(reverse("show_tracker_user", args=(order_id,)))


@csrf_exempt
def change_user_status(request, user_id, what):
    status = "failed"
    user = User.objects.get(pk=user_id)
    if request.user.status == "admin":

        user.status = what
        if what == "admin":
            user.is_staff = True
            user.is_superuser = True
        elif what == "user":
            user.is_staff = False
            user.is_superuser = False
        elif what == "moderator":
            user.is_staff = True
            user.is_superuser = False
        status = "passed"
    user.save()

    return JsonResponse({"status": status, "user_name": user.username, "what": what})


@csrf_exempt
def change_payment_status(request, order_id):
    order = Order.objects.get(pk=order_id)
    status = "failed"

    if request.user.status == "admin" or request.user.status == "moderator":
        order.is_paid = not order.is_paid
        status = "success"
    order.save()
    return JsonResponse({"status": status, "order_status": order.is_paid})


def get_featured_product_info(request):
    web_contents = WebContents.objects.get(pk=1)
    product_1 = Ouds.objects.get(pk=web_contents.featured_product_id_1)
    product_2 = Ouds.objects.get(pk=web_contents.featured_product_id_2)
    product_3 = Ouds.objects.get(pk=web_contents.featured_product_id_3)

    return JsonResponse({"product_1": product_1.serialize(), "product_2": product_2.serialize(), "product_3": product_3.serialize()})
