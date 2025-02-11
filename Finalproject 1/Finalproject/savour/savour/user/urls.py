from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index_view, name="index"),
    path("register/", register, name="register"),
    path("home/", home_view, name="home"),
    path("gallery/",gallery_view, name="gallery"),
    path("uploaditem/",upload_menu_view, name="uploaditem"),
    path("viewitems/", view_menu_view, name="viewitems"),
    path("food_items/", home_view, name="fooditems"),
    path('add_to_cart/<int:menu_item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('order_item/<int:cart_id>/', order_item, name='order_item'),
    path('payment/<int:cart_id>/', payment, name='payment'),
    path('payment/details/', checkout_view, name='paymentdetail'),
    # path('payment_success/<int:cart_id>/', payment_success, name='payment_success'),
    path('reviews', reviews, name="reviews"),
    path('restaurant_reviews/', restaurant_reviews, name="restaurant_reviews"),
    path('uploadtable/', upload_reservation, name='upload_reservation'),
    path('fetchtables/', fetch_reservations, name='fetch_reservations'),
    path('contact/', contact_us_view, name='contact'),
    path('search/', search_view, name='search'),
    path('payment/', payment_view, name='payment_type'),
    path('PaymentDetails/', payment_type, name='payment'),
    path('payment/success/', payment_success_view, name='payment_success'),
    path('table/payment/<int:table_id>', table_payment_view, name="table_payment_view"),
    path('api/cart/<int:item_id>/cancel', cancel_cart_item, name='cancel_cart_item'),
    path('checkout/', checkout_view, name='checkout'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
