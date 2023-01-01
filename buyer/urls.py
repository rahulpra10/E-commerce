from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/",views.about, name= "about"),
    path("contact/",views.contact,name="contact"),
    path("icons/",views.icons,name="icons"),
    path("mens/",views.mens,name="mens"),
    path("single/",views.single,name="single"),
    path("typography/",views.typography,name="typography"),
    path("womens/",views.womens,name="womens"),
    path("otp/",views.otp,name="otp"),
    path("signin/",views.signin,name="signin"),
    path("register/",views.register,name= "register"),
    path("logout/",views.logout,name="logout"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path("add_to_cart/<int:pk>",views.add_to_cart,name="add_to_cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("make_payment/",views.make_payment,name="make_payment"),
    path("make_payment/paymenthandler/",views.paymenthandler,name="paymenthandler"), 
    path("drop_cart_product/<int:pk>",views.drop_cart_product,name="drop_cart_product"),
]
