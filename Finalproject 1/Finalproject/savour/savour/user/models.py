from django.db import models


# Create your models here.
class UserData(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="menu_images/")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('deleted', 'Deleted')
    )
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('net_banking', 'NetBanking'),
        ('credit_card', 'Credit Card'),

    )
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default="pending")
    datetime = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class TableReservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    num_guests = models.IntegerField()
    table_number = models.IntegerField()


class Payments(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    PAYMENT_TYPES = [
        ('U', 'UPI'),
        ('D', 'Debit Card'),
        ('N', 'Net Banking'),
    ]

    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPES)

    # Fields for UPI payment
    upi_id = models.CharField(max_length=50, blank=True, null=True)
    upi_phone_number = models.CharField(max_length=15, blank=True, null=True)
    upi_otp = models.CharField(max_length=10, blank=True, null=True)

    # Fields for Debit Card payment
    debit_card_number = models.CharField(max_length=16, blank=True, null=True)
    cvv = models.CharField(max_length=3, blank=True, null=True)
    debit_card_otp = models.CharField(max_length=6, blank=True, null=True)

    # Fields for Net Banking payment
    bank_account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=11, blank=True, null=True)
    account_holder_name = models.CharField(max_length=100, blank=True, null=True)
    net_banking_otp = models.CharField(max_length=6, blank=True, null=True)

    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    carts = models.ManyToManyField(Cart, related_name='related_%(class)s', blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS)
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {', '.join(str(cart) for cart in self.carts.all())} by {self.user}"

    # def __str__(self):
    #     return f"Payment for {self.cart} by {self.user}"


class Restaurant(models.Model):
    name = models.CharField(max_length=100)


class Reviews(models.Model):
    name = models.CharField(max_length=100)
    reviews_date = models.DateField()
    reviews_time = models.TimeField()
    reviews = models.TextField(null=True)

    def __str__(self):
        return self.name
