from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Buyer,Cart
from django.core.mail import send_mail
import random
from django.conf import settings
from seller.models import Product
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

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
            buyer  = Buyer.objects.get(email = request.session["email"]),
            
            ## create a integer field in htmlhttp://127.0.0.1:8000/ page of Buyer's product div and 
            ## create an a quantity field in MODELS.py :)
        )
        return redirect('index')
    except KeyError:
        # return render(request,"index.html")
        return HttpResponse("sorry")
    except:
        return HttpResponse("Internal server ERROR:")                   




def drop_cart_product(request,pk):
    del_product = Cart.objects.get(id = pk)
    del_product.delete()
    user_obj = Buyer.objects.get(email = request.session["email"])
    cart_product = Cart.objects.filter(buyer = user_obj)
    return render(request,"checkout.html",{"user_obj":user_obj,"cart_product":cart_product, "total_item":len(cart_product)})




def checkout(request):
    if request.method == "GET":
        return render(request,"checkout.html")

    else:
        user_obj = Buyer.objects.get(email = request.session["email"])
        cart_product = Cart.objects.filter(buyer = user_obj)
        return render(request,"checkout.html",{"user_obj":user_obj, 'cart_product':cart_product, "total_item":len(cart_product)})








razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def make_payment(request):

    # /
    # //
    # /
    # /
    # /
    # /
    user_obj = Buyer.objects.get(email = request.session['email'])

    
    #updating quantity from cart page
    session_cart_product = Cart.objects.filter(buyer = user_obj)
    for single_item in session_cart_product: #[fan, ac, fon, tv]
        single_item.quantity = int(request.POST["qua"])
        single_item.save()

    #calculating total price to pay
    cart_product = Cart.objects.filter(buyer = user_obj)
    total_price = 0
    for item in cart_product:
        total_price += item.product.price * int(request.POST["qua"])


    #razorpay stuff
    currency = 'INR'
    global amount
    amount = total_price * 100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['cart_product'] = cart_product
    context['total_price'] = total_price
    return render(request, 'payment.html', context=context)
 
 


@csrf_exempt
def paymenthandler(request):
        # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            
            global amount
            amount = amount  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                session_user = Buyer.objects.get(email = request.session['email'])
                cart_product =  Cart.objects.filter(buyer = session_user)
                for i in cart_product:
                    i.delete()
                # render success page on successful caputre of payment
                return render(request, 'success.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
            
        except:
 
            # if we don't find the required parameters in POST data
            # return HttpResponseBadRequest()
            return HttpResponse("sorry")
    else:
       # if other than POST request is made.
        # return HttpResponseBadRequest()
        return HttpResponse("sorry")
    
def page_not_found(request):
    return render(request,"404.html")

def Interval_server(request):
    return render(request,"500.html")