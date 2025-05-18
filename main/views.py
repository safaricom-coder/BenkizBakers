import json
from django.shortcuts import redirect, render, get_object_or_404

from main.forms import UserProfileForm
from .models import Item,User,UserProfile,Cart,CartItem
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


###########################################


import requests
from django.shortcuts import render, redirect
from django.conf import settings
# from .forms import PaymentForm
from .models import PaymentDetail
from datetime import datetime
from base64 import b64encode
from django.http import JsonResponse

def get_access_token():
    consumer_key = 'Ra1MwZABtTYSg5wvXLPDrIWLjrmNMn58omftsLteoqQAq5Sk'
    consumer_secret = 'zF094FVZxbaD8r3tf6yASIg9kC1u7wsOImj4FwBA6DAhAhPB6eRaBZLgkDL5hmPD'
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    access_token = response.json().get('access_token')
    return access_token


############################################

# Create your views here.
def home(request):

    items = Item.objects.all()
    try:
        cart = Cart.objects.get(user = auth.get_user(request))
    except:
        return render(request,'index.html')
    context = {
        'items':items, 
        'cart':cart,  
      
    }
    return render(request,'index.html',context)

@login_required(login_url='login')
def profile(request):
    user = auth.get_user(request)
    profile = UserProfile.objects.get(user = user)
    context = {
        'profile':profile,
    }
    return render(request,'profile.html',context)

def about(request):
    return render(request,'about.html')


    
@login_required(login_url='login')
def shop(request):
    items = Item.objects.all()
    cart = Cart.objects.get(user = auth.get_user(request))
    
    context = {
        'items':items,
        'cart':cart
    }
    return render(request,'shop.html',context)

def shopdetails(request):
    
    items = Item.objects.all()
    
    context = {
        'items':items
    }
    return render(request,'shop-details.html',context)


@login_required(login_url = 'login')
def shoppingcart(request):
    items = Item.objects.all()
    context = {
        'items':items
    }
    return render(request,'shoppingcart.html',context)


@login_required(login_url = 'login',)
def checkout(request):
    
    cart = Cart.objects.get(user = auth.get_user(request))
    cartitems = CartItem.objects.filter(cart = cart)
    
    context = {
        'cartitems':cartitems,
        'cart':cart,
    }
    return render(request,'checkout.html',context)



def wishlist(request):
    items = Item.objects.all()
    cart = Cart.objects.get(user = auth.get_user(request))
    
    context = {
        'items':items,
        'cart':cart
    }
    return render(request,'wishlist.html',context)



def Class(request):
    items = Item.objects.all()
    context = {
        'items':items
    }
    return render(request,'Class.html',context)



def blogdetails(request):
    items = Item.objects.all()
    context = {
        'items':items
    }
    return render(request,'blogdetails.html',context)

def blog(request):
    items = Item.objects.all()
    context = {
        'items':items
    }
    return render(request,'blog.html',context)



def contact(request):
    items = Item.objects.all()
    context = {
        'items':items
    }
    return render(request,'contact.html',context)

def gallery(request):
    items = Item.objects.all()
    context = {
        'items':items
    }
    return render(request,'cakegallery.html',context)


# actions

def register(request):
    if request.POST:
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
       
        if password1 ==password2:
            if User.objects.filter(email = email).exists():
                messages.info(request,'Email already exists !!')
                return redirect('register')
            elif User.objects.filter(username = username).exists():
                messages.info(request,'Username already taken !!')
                return redirect('register')
            else:
                newuser = User.objects.create_user(username=username,password=password1,email=email)
                profile = UserProfile.objects.create(user = newuser)
                profile.lastname = lastname
                profile.save()
                return redirect('login')
                
        else:
            messages.info(request,"Passwords don't match !!")
            return redirect('register')
            
    return render(request,'register.html') 
   
@login_required(login_url="login")            
def completepurchase(request):
    items = Item.objects.all()
    user = auth.get_user(request)
    
    cart = Cart.objects.get(user=user)
    cart.calcTotal
    cart.save()
    
    profile = UserProfile.objects.get(user = user)
    amount = cart.totalcost
    
    paymentdetail = PaymentDetail.objects.create(profile = profile,amount=amount)
    phone_number = profile.phone_number 
    address = profile.address_or_street
    if (address != '') and phone_number  is not None:
        paymentdetail.paidstatus = True
        paymentdetail.save()
        
        
        cart_total = amount 
        
        if cart_total > 0:
            access_token = get_access_token()
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            business_short_code = '3504296'
            passkey = 'bfb279f9aa9bdbcf113b...YOUR_PASSKEY'
            data_to_encode = business_short_code + passkey + timestamp
            password = b64encode(data_to_encode.encode()).decode()

            stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            payload = {
                "BusinessShortCode": business_short_code,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": cart_total,
                "PartyA": phone_number,
                "PartyB": business_short_code,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://yourdomain.com/api/payment/callback/",
                "AccountReference": "CartCheckout",
                "TransactionDesc": "Paying for cart"
            }

            response = requests.post(stk_push_url, headers=headers, json=payload)
            return JsonResponse(response.json())


        context = {
            'items':items,
        }
        

        return render(request,'shop.html',context)
    else:
        return redirect('updateprofile')

def updateprofile(request):
    user = auth.get_user(request)
    profile = UserProfile.objects.get(user = user)
    form = UserProfileForm(instance=profile)
    
    if request.POST:
        form = UserProfileForm(request.POST,instance=profile)
        
        if form.is_valid():
            
            form.save()
            profile = UserProfile.objects.get(user = user)
            
            return redirect('profile')
        else:
            messages.info(request,"Invalid Data")
            return redirect('updateprofile')
    else:
        context = {
            'form':form,
        }
        return render(request,'updateprofile.html',context)




def login(request):
    if request.method =='POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        
        
        user = auth.authenticate(username=name,password=password)
        
        if user is not None:
            auth.login(request,user)
            newUser = auth.get_user(request)
            try:
                Cart.objects.create(user = newUser)
                return render(request,'home.html')

                
            except:
                
                return redirect('home')
            
        else:
            messages.info(request,'Wrong credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def buyItem(request,pk):
    items = Item.objects.all()
    user = auth.get_user(request)
    try:
        cart = Cart.objects.get(user = user)
    except:
        cart = Cart.objects.create(user = user)
        
    item = Item.objects.get(id = pk)
  
    item.numberOfItems -=1
   
    cart_item = CartItem.objects.create(cart = cart,item=item)
    
    cart_item.quantity +=1
    
    item.save()
    cart_item.save()
    cart.calcTotal
    cart.save()
    context = {
        'items':items,
        'cart':cart
    }
    return render(request,'shop.html',context)


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Process response here
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
    
    
    
