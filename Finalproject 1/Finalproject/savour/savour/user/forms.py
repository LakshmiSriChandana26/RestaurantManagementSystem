from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['username', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ["image", "name", "price", "discounted_price"]


class AddToCartForm(forms.Form):
    menu_item_id = forms.IntegerField()
    quantity = forms.IntegerField(initial=1)


class TableReservationForm(forms.ModelForm):
    class Meta:
        model = TableReservation
        fields = ['name', 'email', 'phone', 'reservation_date', 'reservation_time', 'num_guests', 'table_number']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField(label='Search')


class PaymentDetails(forms.ModelForm):
    class Meta:
        model = Payments
        fields = ["user", "carts", "amount", "payment_type", "payment_status", "transaction_id"]


class PaymentType(forms.Form):
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('net_banking', 'NetBanking'),
        ('credit_card', 'Credit Card'),

    )
    payment_type = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payments

        exclude = ["user", "cart", "amount", "payment_status", "transaction_id", "payment_date"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['name', 'reviews_date', 'reviews_time', 'reviews']
