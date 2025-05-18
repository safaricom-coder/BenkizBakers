import json
from django.shortcuts import redirect, render, get_object_or_404

from main.forms import UserProfileForm,CommentForm
from .models import *
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,request


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


# Create your views here.
def createcontext(request=None):  
    items = Item.objects.all()
    team = UserProfile.objects.filter(is_team = True)
    comments = Comment.objects.all()
    ratings = Rating.objects.all()
    locations = Location.objects.all()
    wishitems ='',
    if request == None:  
       
        context = {
        'items':items,
        'team':team, 
        'comments':comments,
        'ratings':ratings,  
        'locations':locations,  
        }
        return context
    
    elif request:
        wishlists = WishList.objects.all()
        
        if (wishlists.count) == 0:
            pass
        else:
            for obj in wishlists:
                wishlist = obj
                wishitems = WishItem.objects.filter(wishlist = wishlist)
        cart = Cart.objects.get(user = auth.get_user(request))
        
        cartitems = CartItem.objects.filter(cart = cart)
        context = {
        'wishlist':wishlist,
        'items':items,
        'locations':locations,  
        'cartitems':cartitems,
        'team':team, 
        'wishitems':wishitems,
        'comments':comments,
        'cart':cart,  
        'ratings':ratings,  
        'profile':UserProfile.objects.get(user = auth.get_user(request))

        }
        return context
        
def rendercontexttemplate(request,templatename):    
    if request.user.username == '':
        context = createcontext()
        return render(request,f'{templatename}.html',context)
    else:
        context = createcontext(request)
        return render(request,f'{templatename}.html',context)
    
    
def landing(request):
    if request.user.username == '':
        context = createcontext()
        return render(request,'main.html',context)
    else:
        context = createcontext(request)
        return render(request,'main.html',context)
        
def home(request):
    return rendercontexttemplate(request,'main')
@login_required(login_url='login')
def profile(request):
    return rendercontexttemplate(request,'profile')
def about(request):
    return rendercontexttemplate(request,'about')

def shop(request):
    return rendercontexttemplate(request,'shop')
def createcontext2(request):
    profile = UserProfile.objects.get(user = request.user)
    context = {
        'profile':profile,
    }
    return context
class ShopView(generic.ListView):
    model = Item
    template_name = 'shop.html'
    context_object_name = 'things'
    paginate_by = 8
    
    def get_queryset(self):
        return Item.objects.order_by('-id')
    
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update(createcontext())
        context.update(createcontext2(self.request))
        return context
        
        
@login_required(login_url='login')
def shop(request):
    return rendercontexttemplate(request,'shop')

def shopdetails(request):
    return rendercontexttemplate(request,'shop-details')
@login_required(login_url = 'login')
def shoppingcart(request):
    return rendercontexttemplate(request,'shoppingcart')
@login_required(login_url = 'login',)
def checkout(request):
    return rendercontexttemplate(request,'checkout')
@login_required(login_url='login')
def wishlist(request):
    return rendercontexttemplate(request,'wishlist')
@login_required(login_url='login')
def addToWishlist(request,id):
    item = Item.objects.get(id = id)
    user = auth.get_user(request)
    #  check existance
    if WishList.objects.filter(user = user).exists():
        wishlist = WishList.objects.get(user = user)
        wishitem = WishItem.objects.create(item = item)
        wishitem.wishlist = wishlist
        wishitem.save()
        wishlist.save()
        return redirect('shop')
    else:
        
        return redirect('shop')
    
@login_required(login_url='login')    
def removewishitem(request,pk):
    wishlist = WishList.objects.get(user = auth.get_user(request))
    wishitems = WishItem.objects.filter(wishlist = wishlist)
    
    for item in wishitems:
        if WishItem.objects.get(id=pk):
            WishItem.objects.get(id=pk).delete()
            return redirect('wishlist')
            
def Class(request):
    return rendercontexttemplate(request,'Class')

def blogdetails(request):
    return rendercontexttemplate(request,'blogdetails')

def blog(request):
    return rendercontexttemplate(request,'blog')
    
def contact(request):
    return rendercontexttemplate(request,'contact')

def gallery(request):
    return rendercontexttemplate(request,'cakegallery')


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
                usser = User.objects.get(username = username)
                Cart.objects.create(user = usser)
                WishList.objects.create(user = usser)
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
    amount = int(cart.totalcost)
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
            business_short_code = '174379'
            passkey = 'bfb279f9aa9bdbcf113bMTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjUwNTExMTIwNzUx'
            data_to_encode = business_short_code + passkey + timestamp
            password = b64encode(data_to_encode.encode()).decode()

            stk_push_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
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
                "AccountReference": "BenkizBakers",
                "TransactionDesc": "Paying for Purchase from Benkiz Bakers"
            }

            response = requests.post(stk_push_url, headers=headers, json=payload)
            print(f"""
            
            {payload}
""")
            return JsonResponse(response.json())
        context = createcontext(request)

        return render(request,'shop.html',context)
    else:
        return redirect('updateprofile')

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Process response here
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
    

def updateprofile(request):
    user = auth.get_user(request)
    profile = UserProfile.objects.get(user = user)
    form = UserProfileForm(instance=profile)
    
    if request.POST:
        form = UserProfileForm(request.POST,request.FILES,instance=profile)
    
        if form.is_valid():
            form.save()
            
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
            user = auth.get_user(request)
            if Cart.objects.filter(user=user).exists():
                return redirect('home')
            else:
                Cart.objects.create(user = user)
                return redirect('home')
        else:
            messages.info(request,f"Wrong credentials for **{name.upper()}** .")
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def buyItem(request,pk):
    items = Item.objects.all()
    user = auth.get_user(request)
    cart = Cart.objects.get(user = user)
    item = Item.objects.get(id = pk)
    item.numberOfItems -=1
    cart_item = CartItem.objects.filter(cart = cart,item=item).exists()
    if cart_item :
        cart_item = CartItem.objects.get(cart = cart,item = item)
    else:
        cart_item = CartItem.objects.create(cart = cart,item = item)
    
    cart_item.quantity +=1
    item.save()
    cart_item.save()
    cart.calcTotal
    cart.save()
    return rendercontexttemplate(request,'shop')

@login_required(login_url='login')
def createcomment(request):
    form = CommentForm()
    profile = UserProfile.objects.get(user = request.user)
    if request.method == "POST":
        userr = auth.get_user(request)
        instance = Comment.objects.create(user = userr,profile = UserProfile.objects.get(user = userr))
        form = CommentForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            messages.info(request,'Comment is saved !')
            return redirect ("home")
        
    comments = Comment.objects.all()
    for comment in comments:
        print(comment.user.username * 20)
    
    context = {
        'form':form,
        'comments':comments,
        'profile':profile,
    }
    return render(request,'commentrate.html',context)
