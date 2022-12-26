from django.urls import path
from .import views

urlpatterns = [
    path("index/",views.seller_index,name="seller_index"),
    path("seller_register/",views.seller_register,name="seller_register"),
    path("seller_otp/",views.seller_otp,name="seller_otp"),
    path("seller_signin/",views.seller_signin,name="seller_signin"),
    path("seller_edit_profile/",views.seller_edit_profile,name="seller_edit_profile"),
    path("seller_logout/",views.seller_logout,name="seller_logout"),
    path("add_product/",views.add_product,name="add_product"),
    
    
]
