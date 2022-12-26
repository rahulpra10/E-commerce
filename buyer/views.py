from django.shortcuts import render,redirect,HttpResponse
from .models import Buyer,Cart
from django.core.mail import send_mail
import random
from django.conf import settings
from seller.models import Product

# Create your views here.

# for home page:
def index(request):
    all_product = Product.objects.all()
    try:
        user_obj = Buyer.objects.get(email = request.session['email'])
        return render(request, "index.html",{"user_obj": user_obj,"all_product":all_product})
    except:
        return render(request,"index.html",{"all_product":all_product})


def register(request):

    if request.method == "GET":
        return render(request, "index.html")

    elif request.method == "POST":
        if len(request.POST["password"]) < 8:
            return render(request, "index.html",{"massage":"Password is too short!! at least 8 charcter requird:"})

        elif request.POST["password"] == request.POST["re_password"]:
            try:
                user_mail = Buyer.objects.get(email = request.POST["email"])
                return render(request, "index.html",{"massage": "This email is already exist! please use another email:"})
            except:
                global user_dict
                user_dict = {
                    "first_name": request.POST["f_name"],
                    "last_name": request.POST["l_name"],
                    "Address":request.POST["address"],
                    "Email":request.POST["email"],
                    "Contact":request.POST["contact"],
                    "Password":request.POST["password"],
                    "Re_password": request.POST["re_password"],

                    }

                

                subject = "Registration!!!"
                global gen_otp
                gen_otp = random.randint(100000,999999)
                massage = f''' Hello {user_dict["first_name"].upper()}.
                Your otp is {gen_otp}.'''
                from_email = settings.EMAIL_HOST_USER
                list1 = [request.POST["email"]]
                send_mail(subject,massage,from_email,list1)
                return render (request, "otp.html",{"massage":"Please check your mailbox"})

        else:
            return render(request, "index.html",{"massage":"Password and confirm password are not match!!Enter AGAIN:"})



def otp(request):
    
    
    if request.method == "POST":
        if gen_otp == int(request.POST["otp"]):
            Buyer.objects.create(

            first_name = user_dict["first_name"],
            last_name = user_dict["last_name"],
            address = user_dict["Address"],
            email =user_dict["Email"],
            mobile =  user_dict["Contact"],
            password = user_dict["Password"],
    
           )
            
            return render(request, "index.html",{"massage":"Your Register successfull go and sing IN:"})

        else:
            return render(request, "otp.html",{"massage":"Your OTP is incorrect!! ENTER OTP AGAIN: "})

    else:
        return render(request, "index.html")




#for about page:
def about(request):
    return render(request, "about.html")

#for contact page:
def contact(request):
    return render(request,"contact.html")

#for icons page:
def icons(request):
    return render(request,"icons.html")

#for mens page:
def mens(request):
    return render(request,"mens.html")

#for single page:
def single(request):
    return render(request,"single.html")

# for typography page:
def typography(request):
    return render(request,"typography.html")

# for women's page:
def womens(request):
    return render(request,"womens.html")



def signin(request):
    if request.method == "GET":
        return render(request, "index.html")
    
    else:
        try:
            session_user = Buyer.objects.get(email = request.POST["email"])
            if request.POST["password"] == session_user.password:
                request.session["email"] = request.POST["email"]
                return redirect("index")

            else:
                return render(request, "index.htmt",{"massage":"TRY AGAIN!!! Pasword is INCORRECT:"})


        except:
            return render(request,"index.html",{"massage":"This Email is not EXIST !! Please register First or Enter correct Email:"})
           



#for edit_profile option 
def edit_profile(request):
    if request.method == "GET":
        try:
            user_obj = Buyer.objects.get(email=request.session["email"])
            return render(request,"edit_profile.html",{"user_obj":user_obj})
        except:
            return render(request,"index.html")
            
    else:
        user_obj= Buyer.objects.get(email= request.session["email"])
        user_obj.first_name = request.POST["f_name"]  
        user_obj.last_name = request.POST["l_name"]
        user_obj.address = request.POST["address"]
        user_obj.mobile = request.POST["contact"]
        user_obj.gender = request.POST["gender"]
        user_obj.dob = request.POST["dob"]
        if request.FILES:
            user_obj.pic = request.FILES["pic"]
        user_obj.save()
        user_obj= Buyer.objects.get(email= request.session["email"])
        return render(request,"index.html",{"user_obj":user_obj})
        


    

# for logout
def logout(request):
    del request.session["email"]
    return render(request,"index.html")



def add_to_cart(request,pk):
    try:
        Cart.objects.create(
            product = Product.objects.get(id = pk),
            buyer = Buyer.objects.get(email = request.session["email"]),
            quantity = request.GET[str(pk)]
            ## create a integer field in html page of Buyer's product div and 
            ## create an a quantity field in MODELS.py :)
        )
        return redirect('index')
    except KeyError:
        # return render(request,"index.html")
        return HttpResponse("sorry")
    except:
        return HttpResponse("Internal server ERROR:")                   

#  try:
#         Cart.objects.create(
#             product = Product.objects.get(id = pk),
#             buyer = Buyer.objects.get(email = request.session['email']),
#             quantity = request.GET[str(pk)]
#         )
#         return redirect('index')
#     except KeyError:
#         return render(request, 'login.html')
#     except:
#         return render(request, '500.html')
    