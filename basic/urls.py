from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static
import secrets
num = 55245

urlpatterns = [
    path("", views.home, name="home"),
    path("shop", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register/verify_contact", views.verify_contact, name="verify_contact"),
    path("aboutus", views.show_aboutus, name="aboutus"),
    path("update_amount/<int:oud_id>", views.update_amount, name="update_amount"),
    path("category/update_amount/<int:oud_id>", views.update_amount, name="update_amount"),
    path("oud_page/<int:oud_id>", views.oud_page, name="oud_page"),
    path("review/<int:oud_id>", views.review, name="review"),
    path("oud_page/update_amount/<int:oud_id>", views.update_amount, name="update_amount"),
    path("cart", views.show_cart, name="show_cart"),
    path("take_order", views.take_order, name="take_order"),
    path("tracker", views.show_tracker, name="show_tracker"),
    path("exclusive", views.exclusive, name="exclusive"),
    path("category/<str:category_name>", views.category, name="category"),
    path("search", views.search, name = "search"),
    path("contact_us", views.contact_us, name="contact_us"),
    path("slider", views.test_slider, name="slider"),
    path("admin_page/" + str(num) + "/", views.admin_page, name="admin_page"),
    path("admin_page/" + str(num) + "/update_amount/<int:oud_id>", views.update_amount, name="admin_page_update_amount"),
    path("admin_page/" + str(num) + "/edit_oud/<int:oud_id>", views.edit_ouds, name="edit_oud"),
    path("admin_page/" + str(num) + "/add_oud", views.add_oud, name="add_oud"),
    path("promo_check/<str:promo_code>", views.check_promo, name="check_promo"),
    path("admin_page/" + str(num) + "/change_content", views.change_content, name="change_content"),
    path("admin_page/" + str(num) + "/change_visibility/<int:oud_id>", views.change_visibility, name="change_visibility"),
    path("admin_page/" + str(num) + "/delete_record/<str:what>/<int:nice_id>", views.delete_record, name="delete_record" ),
    path("show_order/<int:order_id>", views.show_order, name="show_order_user"),

    #all tracker related requests
    path("show_order/<int:order_id>/tracker", views.show_trac, name="show_tracker_user"),
    path("show_order/<int:order_id>/change_payment_status", views.change_payment_status, name="payment_status"),
    path("show_order/<int:order_id>/tracker/<int:value>", views.change_trac_value, name="show_tracker_user_value"),
    path("show_order/<int:order_id>/change_delivery", views.change_delivery_date, name="change_delivery_date"),
    path("show_order/<int:order_id>/change_delivery_status/<str:what>", views.change_payment_status, name="payment_status"),


    path("admin_page/" + str(num) + "/show_order/<int:order_id>", views.show_order, name="show_order_admin"),

    path("aboutus/get_webcontents", views.show_content, name="get_contents" ),
    path("admin_page/" + str(num) + "/add_category", views.add_category, name="add_category"),
    path("admin_page/" + str(num) + "/add_promo", views.add_promo, name="add_promo"),
    path("admin_page/" + str(num) + "/add_quantity", views.add_quantity, name="add_quantity"),
    path("admin_page/" + str(num) + "/edit/<str:what>/<int:nice_id>", views.edit_record, name="edit_records"),
    path("admin_page/" + str(num) + "/add_notice", views.add_notice, name="add_notice"),

    path("cancel_order/<int:order_id>", views.cancel_order, name="cancel_order"),
    path("profile_page/<int:user_id>", views.show_profile_page, name="profile_page"),
    path("profile_page/<int:user_id>/edit/<str:what>/<int:nice_id>", views.edit_shipping, name="edit_records_user"),
    path("add_shipping", views.add_shipping, name="add_shipping"),
    path("change_profile/<int:user_id>", views.change_profile, name="change_profile"),
    path("admin_page/"+ str(num) +  "/change_user_status/<int:user_id>/<str:what>", views.change_user_status, name="change_status"),
    path("sendmail", views.send_email_to_user, name="send_email"),




    # payment messages
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),  
]