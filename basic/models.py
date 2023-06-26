from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
import os


class User(AbstractUser):
    status = models.CharField(max_length=100, default="user")
    img = models.ImageField(null=True, blank=True,upload_to="images/")
    full_name = models.CharField(max_length=1000, default="Raihan Rashid")
    contact_no = models.CharField(max_length=20, default="01746695655")
    gender = models.CharField(max_length=6, default="male")
    points = models.IntegerField(default=0)
    has_shipping = models.BooleanField(default = False)
    default_shipping_id = models.IntegerField(default=0)


class QuantityManagement(models.Model):
    amount = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"{self.amount}"
    def serialize(self):
        return {
            "amount" : self.amount,
        }


class Categories(models.Model):
    name = models.CharField(max_length=50, default="No Categories")
    def __str___(self):
        return f"{self.name}"
    
    def serialize(self):
        return {
            "name" : self.name,
        }

class Ouds(models.Model):
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=5, default="open")
    description = models.CharField(max_length=3000)
    exerpt = models.CharField(max_length=150, default="nice")
    base_price=models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    amount = models.DecimalField(max_digits=10, decimal_places = 2, default = "2.5")
    base_amount = models.DecimalField(max_digits=10, decimal_places=2, default="2.5")
    price_1 = models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    price_2 = models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    price_3 = models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    price_4 = models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    prev_price_1 = models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    prev_price_2 = models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    prev_price_3 = models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    prev_price_4 = models.DecimalField(max_digits=30,decimal_places=2, default="000000.00")
    offer_status = models.CharField(max_length=10, default="closed")
    offer_amount = models.IntegerField(default="50")
    img = models.ImageField(null=True, blank=True,upload_to="images/")
    cover_image1 = models.ImageField(null=True, blank=True,upload_to="images/")
    category= models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    amount_type = models.ManyToManyField(QuantityManagement)
    amount_number = models.IntegerField(default="3")
    tags = models.CharField(max_length=1000, default = "")
    inventory = models.DecimalField(max_digits=30, decimal_places=2, default="100.00")
    total_sold = models.IntegerField(default=0)
    visibility = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} {self.description} ${self.base_price}"

    def serialize(self):
        return {
            "id" : self.id,
            "img_url" : self.img.url,
            "title" : self.title,
            "base_price" : self.base_price,
            "amount" : self.amount,
            "base_amount" : self.base_amount,
            "price_1" : self.price_1,
            "price_2" : self.price_2,
            "price_3" : self.price_3,
            "price_4" : self.price_4,
            "prev_price_1" : self.prev_price_1,
            "prev_price_2" : self.prev_price_2,
            "prev_price_3" : self.prev_price_3,
            "prev_price_4" : self.prev_price_4,
            "visibility" : self.visibility,
        }
    
    """
    
    def delete(self, *args, **kwargs):
        # Delete the associated image file
        if self.img:
            # Get the path to the image file
            image_path = self.img.path

            # Delete the file from the file system
            if os.path.exists(image_path):
                os.remove(image_path)

        if self.cover_image1:
            image_path2 = self.cover_image1.path
        
        if os.path.exists(image_path2):
            os.remove(image_path2)

        # Call the superclass delete() method to delete the record
        super().delete(*args, **kwargs)
    """


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oud = models.ForeignKey(Ouds, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.review}"


class Order(models.Model):
    order = models.CharField(max_length=5000)
    total_price = models.DecimalField(max_digits=30, decimal_places=2, default="100")
    payment_method = models.CharField(max_length=100, default="Cash On Delivery")
    delivery_charge = models.DecimalField(max_digits=20, decimal_places=2, default="0.00")
    promo_discount = models.DecimalField(max_digits=30, decimal_places=2, default="0.00")
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    area = models.CharField(max_length=200, default="none")
    town = models.CharField(max_length=200, default="none")
    transaction_id = models.CharField(max_length=500, default="none")
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default="not delivered")
    reason_for_cancellation = models.CharField(max_length=200, default="none")

    # def __str__(self):
    #     return f"{self.id}"
    
    def serialize(self):
        return {
            "status" : self.status,
        }

class Tracker(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    desc = models.CharField(max_length=5000)
    progress = models.IntegerField(default="0")
    order_date = models.DateField(editable = True, auto_now_add=True)
    delivary_date = models.DateField(blank=True, default=datetime.date.today())
    def __str__(self):
        return f"{self.id}"



class ContactUs(models.Model):
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=20)
    message = models.CharField(max_length=5000)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.email}"


class WebContents(models.Model):
    aboutus = models.CharField(max_length=10000)
    privacy_policy = models.CharField(max_length=10000)
    payment_policy = models.CharField(max_length=10000)
    shipping_policy = models.CharField(max_length=10000)
    term_and_conditions = models.CharField(max_length=10000)
    exchange_and_return = models.CharField(max_length=10000)
    delivery_charge = models.IntegerField()
    contact_no = models.CharField(max_length=20)
    contact_no_2 = models.CharField(max_length=20, default="0915485")
    email = models.CharField(max_length=100)
    featured_product_id_1 = models.CharField(max_length=10)
    featured_product_id_2 = models.CharField(max_length=10)
    featured_product_id_3 = models.CharField(max_length=10)

    def serialize(self):
        return {
            "aboutus" : self.aboutus,
            "privacy_policy" : self.privacy_policy,
            "payment_policy" : self.payment_policy,
            "shipping_policy" : self.shipping_policy,
            "terms_and_conditions" : self.term_and_conditions,
            "exchange_and_return" : self.exchange_and_return,
            "delivery_charge" : self.delivery_charge,
            "contact_no" : self.contact_no,
            "contact_no_2" : self.contact_no_2,
            "email" : self.email,
            "featured_product_id_1" : self.featured_product_id_1,
            "featured_product_id_2" : self.featured_product_id_2,
            "featured_product_id_3" : self.featured_product_id_3,
        }


class Promos(models.Model):
    name = models.CharField(max_length=100)
    discount_amount = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return f"{self.id} {self.name} {self.discount_amount}"

    def serialize(self):
        return {
            "name" : self.name,
            "discount" : self.discount_amount,
        }


class UserOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete= models.CASCADE)


class Moderators(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    area = models.CharField(max_length=200, default="none")
    town = models.CharField(max_length=200, default="none")
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id} {self.name} {self.city}"
    

class Analytics(models.Model):
    total_sale = models.IntegerField()
    total_credits = models.DecimalField(max_digits=30, decimal_places=2)
    total_stock = models.IntegerField()
    total_orders = models.IntegerField()
    total_deliveries = models.IntegerField()


