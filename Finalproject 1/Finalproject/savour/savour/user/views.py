

from django.db.models import *
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import MenuItemForm, ContactForm, TableReservationForm, ReviewForm
from .forms import LoginForm, RegistrationForm


# Create your views here.
from .models import *
from .forms import *
import uuid

def index_view(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            userdata = UserData.objects.get(username=uname)
            if userdata.password == pwd:
                request.session["user"] = userdata.id
                request.session["name"] = userdata.username.capitalize()
                print("trying to go home")
                return redirect("home")
            else:
                loginform = LoginForm
                message = "Incorrect Password!"
                messages.error(request, message)
                # return render(request, "index.html", {"loginform": loginform, "message": message})
        except Exception as e:
            print(e)
            loginform = LoginForm
            messages.error(request, "Username Doesn't Exists!")
            # message = "Email Doesn't Exists!"
            # return render(request, "index.html", {"loginform": loginform, "message": message})
    loginform = LoginForm
    return render(request, "index.html", {"loginform": loginform})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the desired page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def home_view(request):
    name_ = request.session["name"].capitalize()
    menu_items = FoodItem.objects.all()
    return render(request, "fooditems.html", {"uname": name_, "menu_items": menu_items})


def food_items(request):
    return render(request, "fooditems.html")


def gallery_view(request):
    return render(request, "gallery.html")


def upload_menu_view(request):
    print("I camee")
    if request.method == "POST":
        print("I am in post")
        form = MenuItemForm(request.POST, request.FILES)
        print("form", form)
        if form.is_valid():
            print("Iam valid")
            form.save()
            menu_items = FoodItem.objects.all()
            return render(request, "upload_menu.html", {"form": form, "menu_items": menu_items})
            # return redirect('viewitems')  # Redirect to the view menu page after successful upload
    else:
        print("Iam in get")
        form = MenuItemForm()
        menu_items = FoodItem.objects.all()
        return render(request, "upload_menu.html", {"form": form, "menu_items": menu_items})


def view_menu_view(request):
    menu_items = FoodItem.objects.all()
    return render(request, "view_menu.html", {"menu_items": menu_items})


def add_cart(request):
    cart_items = CartItem.objects.all()
    return render(request, 'cart.html', {'cart_items': cart_items})


def cart_view(request):
    if request.method == "POST":
        print("data", request.POST)
        return render(request, 'cart.html')

    # Retrieve cart data from session
    cart_items = request.session.get('cart_items', [])
    print(cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items})


def add_to_cart(request, menu_item_id):
    user_id = request.session["user"]
    print(user_id)
    user_profile = UserData.objects.get(
        id=user_id)  # Assuming you have a one-to-one relationship with UserProfile

    menu_item = FoodItem.objects.get(pk=menu_item_id)
    print("kkk", user_profile, menu_item, "kkk")
    quantity = int(request.POST['quantity'])

    # Create a new Cart object with user profile, menu item, and quantity information
    cart = Cart.objects.create(user=user_profile, menu_item=menu_item, quantity=quantity)

    print(cart)

    # Redirect to the cart detail page
    return redirect('cart_detail')


def cart_detail(request):
    # Retrieve the user's cart items
    user_id = request.session["user"]
    print(user_id)
    cart_items = Cart.objects.filter(user=user_id).exclude(Q(status='completed') | Q(status='deleted'))
    #cart_items = Cart.objects.filter(user=user_id).exclude(status='ordered')
    print(cart_items)
    return render(request, 'cart_details.html', {'cart_items': cart_items})


def order_item(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)

    return redirect('payment', cart_id=cart.id)


def payment(request, cart_id):
    cart = Cart.objects.get(id=cart_id)

    total_amount = cart.menu_item.price * cart.quantity

    return render(request, 'payment.html', {'cart': cart, 'total_amount': total_amount})


def payment_success(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.status = 'completed'
    cart.save()
    return render(request, 'payment_success.html', {"cart": cart})


def contact(request):
    return render(request, "contact.html")

def reviews(request):
    if request.method == 'POST':
        print(request.POST)
        form = ReviewForm(request.POST)
        print(form.is_valid(), form.errors)
        if form.is_valid():
            form.save()  # Save the review to the database
            return redirect('home')  # Redirect to see the updated reviews
    else:
        form = ReviewForm()
    return render(request, "reviews.html", {'form': form})


def restaurant_reviews(request):
    # if request.method == "POST":
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         redirect("home")
    reviews = Reviews.objects.all()  # Capitalized "Reviews"
    return render(request, 'restaurant_reviews.html', { 'reviews': reviews})
    # who and where to give reviews?
# reviews have no data now


def upload_reservation(request):
    if request.method == 'POST':
        form = TableReservationForm(request.POST)
        print(form.is_valid(), form.errors)
        if form.is_valid():
            id_ = form.save()
            return redirect('table_payment_view', id_.id)
    else:
        form = TableReservationForm()
    return render(request, 'upload_reservation.html', {'form': form})


def fetch_reservations(request):
    reservations = TableReservation.objects.all()
    return render(request, 'fetch_reservation.html', {'reservations': reservations})


def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (send email, save to database, etc.)
            return redirect('fooditems')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def search_view(request):
    query = request.POST.get('query')
    name_ = request.session["name"]
    print(query)
    menu_items = []
    if query:
        menu_items = FoodItem.objects.filter(name__icontains=query.lower())
    # return render(request, 'search_results.html', {'results': results})

    return render(request, "fooditems.html", {"uname": name_, "menu_items": menu_items})


def payment_view(request, cart_id):
    print("in payment view func", cart_id)
    print("input is: ", request.POST)
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        print(form.is_valid(), form.errors)
        if form.is_valid():
            payment_type = form.cleaned_data['payment_type']
            cart = get_object_or_404(Cart, id=cart_id)

            total_amount = cart.menu_item.price * cart.quantity
            print(payment_type, total_amount)
            transaction_id = uuid.uuid4().hex
            print(request.POST.dict())
            data = request.POST.dict()
            data.pop("csrfmiddlewaretoken")
            print(data)
            data.update({"user": cart.user, "cart": cart, "amount": total_amount, "payment_type": payment_type,
                         "payment_status": "completed", "transaction_id": transaction_id})
            Payments.objects.create(**data)
            # Process payment based on the selected payment type
            # This is where you would typically integrate with a payment gateway or handle the payment logic
            # Redirect to a success page or do further processing
            cart.status = 'completed'
            cart.save()
            return redirect('payment_success')
    else:
        form = PaymentForm()
        # form = PaymentForm()
    cart_data = Cart.objects.get(id=cart_id)
    return render(request, 'paytype.html', {'form': form, "cart": cart_data})


def checkout_view(request):
    # print(cart_items)
    # cart_ids = request.GET.getlist('cart_ids')  # Retrieve cart IDs from query parameters
    # cart_items = Cart.objects.filter(id__in=cart_ids)
    # total_price = sum(item.menu_item.price * item.quantity for item in cart_items)
    # context = {
    #     'cart_items': cart_items,
    #     'total_price': total_price,
    # }
    # return render(request, 'checkout.html', context)
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        print(form.is_valid(), form.errors)
        if form.is_valid():
            payment_type = form.cleaned_data['payment_type']
            print("in checkput view", request.session["user"])
            cart_items = Cart.objects.filter(user__id=request.session["user"], status='pending')
            total_amount = sum(item.menu_item.price * item.quantity for item in cart_items)
            print(payment_type, total_amount)
            transaction_id = uuid.uuid4().hex
            print(request.POST.dict())
            data = request.POST.dict()
            data.pop("csrfmiddlewaretoken")
            print(data)
            data.update({"user": cart_items[0].user, "amount": total_amount, "payment_type": payment_type,
                         "payment_status": "completed", "transaction_id": transaction_id})
            #Payments.objects.create(**data)
            # Create a new Payments instance
            payment = Payments.objects.create(**data)

            # Associate the cart_items with the Payments instance
            payment.carts.add(*cart_items)
            # Process payment based on the selected payment type
            # This is where you would typically integrate with a payment gateway or handle the payment logic
            # Redirect to a success page or do further processing
            for cart in cart_items:
                cart.status = 'completed'
                cart.save()
            return redirect('payment_success')
    else:
        form = PaymentForm()
        # form = PaymentForm()
    cart_data = Cart.objects.filter(user__id=request.session["user"], status='pending')
    return render(request, 'paytype.html', {'form': form, "cart_items": cart_data})


def payment_type(request):
    if request.method == 'POST':
        form = PaymentType(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_success')  # Redirect to a success page
    else:
        form = PaymentType()
    return render(request, 'payment_type.html', {'form': form})


def payment_success_view(request):
    # This view can be used to display a success message after payment is processed
    return render(request, 'payment_success.html')


def logout_view(request):
    request.session.clear()
    return redirect('index')


def table_payment_view(request, table_id):
    print("in payment view func", table_id)
    print("input is: ", request.POST)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        print(form.is_valid(), form.errors)
        if form.is_valid():
            payment_type = form.cleaned_data['payment_type']
            total_amount = 250
            print(payment_type, total_amount)
            transaction_id = uuid.uuid4().hex
            print(request.POST.dict())
            data = request.POST.dict()
            data.pop("csrfmiddlewaretoken")
            print(data)
            cart = TableReservation.objects.get(id=table_id)
            data.update({"user": cart.user, "cart": cart, "amount": total_amount, "payment_type": payment_type,
                         "payment_status": "completed", "transaction_id": transaction_id})
            Payments.objects.create(**data)

            return redirect('payment_success')
    else:
        form = PaymentForm()
        # form = PaymentForm()
    cart_data = TableReservation.objects.get(id=table_id)
    return render(request, 'paytype.html', {'form': form, "cart": cart_data})


@require_http_methods(["PUT"])
def cancel_cart_item(request, item_id):
    print("cancel item request came", item_id)
    try:
        cart_item = Cart.objects.get(pk=item_id)
        cart_item.status = 'deleted'
        cart_item.save()
        return JsonResponse({'message': 'Cart item cancelled successfully'}, status=200)
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
