from django.shortcuts import render,redirect,HttpResponse
from .models import Seller,Product
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.
def seller_index(request):
    try:
        seller_obj = Seller.objects.get(email=request.session["email"])
        return render(request, "seller_index.html",{"seller_obj": seller_obj })
    except:
        return render(request,"seller_index.html")
        # return HttpResponse("hiiii how are you")
        

    

def seller_register(request):

    if request.method == "GET":
        return render(request, "seller_index.html")

    elif request.method == "POST":
        if len(request.POST["password"]) < 8:
            return render(request, "seller_index.html",{"massage":"Password is too short!! at least 8 charcter requird:"})

        elif request.POST["password"] == request.POST["re_password"]:
            try:
                seller_email = Seller.objects.get(email = request.POST["email"])
                return render(request, "seller_index.html",{"massage": "This email is already exist! please use another email:"})
            except:
                global seller_dict
                seller_dict = {
                    "first_name": request.POST["f_name"],
                    "last_name": request.POST["l_name"],
                    "Address":request.POST["address"],
                    "Email":request.POST["email"],
                    "Contact":request.POST["contact"],
                    "Password":request.POST["password"],
                    "Re_password": request.POST["re_password"],
                   

                }
                subject = "Registration!!!"
                global generated_otp
                generated_otp = random.randint(100000,999999)
                massage = f''' Hello {seller_dict["first_name"].upper()}.
                Your otp is {generated_otp}.'''
                from_email = settings.EMAIL_HOST_USER
                list1 = [request.POST["email"]]
                send_mail(subject,massage,from_email,list1)
                return render (request, "seller_otp.html",{"massage":"Please check your mailbox"})

        else:
            return render(request, "seller_index.html",{"massage":"Password and confirm password are not match!!Enter AGAIN:"})



def seller_otp(request):
    
    if request.method == "POST":
        global generated_otp
        if generated_otp == int(request.POST["seller_otp"]):
            Seller.objects.create(

                first_name = seller_dict["first_name"],
                last_name = seller_dict["last_name"],
                address = seller_dict["Address"],
                email =seller_dict["Email"],
                mobile =  seller_dict["Contact"],
                password = seller_dict["Password"],
                
                
                )
            return render(request, "seller_index.html",{"massage":"Your Register successfull go and sing IN:"})

        else:
            return render(request, "seller_otp.html",{"massage":"Your OTP is incorrect!! ENTER OTP AGAIN: "})

    else:
        return render(request, "seller_index.html")

def seller_signin(request):
    if request.method == "GET":
        return render(request, "seller_index.html")
    
    else:
        try:
            session_seller = Seller.objects.get(email = request.POST["email"])
            if request.POST["password"] == session_seller.password:
                request.session["email"] = request.POST["email"]
                return redirect("seller_index")

            else:
                return render(request, "seller_index.htmt",{"massage":"TRY AGAIN!!! Pasword is INCORRECT:"})


        except:
            return render(request,"seller_index.html",{"massage":"This Email is not EXIST !! Please register First or Enter correct Email:"})
            # return HttpResponse("sorrry budyy:")
           
def seller_edit_profile(request):
    if request.method == "GET":
        try:
            seller_obj = Seller.objects.get(email = request.session["email"])
            return render(request,"seller_edit_profile.html",{"seller_obj":seller_obj})
        except:
            return render(request,"seller_index.html")
    else:
        seller_obj = Seller.objects.get(email=request.session["email"])
        seller_obj.first_name = request.POST["f_name"]  
        seller_obj.last_name = request.POST["l_name"]
        seller_obj.address = request.POST["address"]
        seller_obj.mobile = request.POST["contact"]
        seller_obj.gender = request.POST["gender"]
        seller_obj.dob = request.POST["dob"]
        if request.FILES:
            seller_obj.pic = request.FILES["pic"]
        seller_obj.save()
        seller_obj = Seller.objects.get(email=request.session["email"])
        return render(request,"seller_index.html",{"seller_obj": seller_obj})
        


def seller_logout(request):
    del request.session["email"]
    return render(request,"seller_index.html")



def add_product(request):
    if request.method == "GET":
        try:
            seller_obj = Seller.objects.get(email = request.session["email"])
            return render(request,"add_product.html",{"seller_obj":seller_obj})

        except:
            return render(request, "seller_index.html" )
    else:
        seller_obj = Seller.objects.get(email = request.session["email"])


        # for calcute the DISCOUNT (
        price = int(request.POST["price"])
        discount =int(request.POST["discount"])
        dis_price  = price - (price * (discount / 100))

        

        Product.objects.create(
            p_name = request.POST["p_name"],
            des = request.POST["des"],
            price = request.POST["price"],
            dis_price = dis_price ,
            qua = request.POST["qua"],
            pic = request.FILES["pic"]
        )

      
        return render(request,"add_product.html",{"massage":"successfully added!!","seller_obj":seller_obj, })







            ## for loop  for product display 
        # {% for item in all_products %}
		# 						<div class="col-md-4 product-men mt-5">
		# 							<div class="men-pro-item simpleCart_shelfItem">
		# 								<div class="men-thumb-item text-center">
		# 									<img src="{{item.pic.url}}" alt="">
		# 									<div class="men-cart-pro">
		# 										<div class="inner-men-cart-pro">
		# 											<a href="single.html" class="link-product-add-cart">Quick View</a>
		# 										</div>
		# 									</div>
		# 								</div>
		# 								<div class="item-info-product text-center border-top mt-4">
		# 									<h4 class="pt-1">
		# 										<a href="single.html">{{item.name}}</a>
		# 									</h4>
		# 									<div class="info-product-price my-2">
		# 										<span class="item_price">${{item.price}}</span>
												
		# 									</div>
		# 									<div class="snipcart-details top_brand_home_details item_add single-item hvr-outline-out">
		# 									<form action="{% url 'add_to_cart' item.id %}">
		# 									<input type="number" name="{{item.id}}">
		# 									<button type="submit" class="button btn">Add to Cart</button>
		# 									</form>	
		# 									</div>
		# 								</div>
		# 							</div>
		# 						</div>
		# 						{% endfor %}