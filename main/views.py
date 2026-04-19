import json
from django.shortcuts import redirect, render, get_object_or_404

from main.forms import UserProfileForm
from .models import *
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,request
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views import View
from main import urls
import requests
# from djago.core.files.storage import FileSysteStorage

###########################################

from django.shortcuts import render, redirect
from django.conf import settings
from .forms import *
# from .models import PaymentDetail
from datetime import datetime
from base64 import b64encode
from django.http import JsonResponse
# from benkizapi.views import handle_payment_callback
from benkizapi.views import handle_payment_callback

import os
api_key = os.environ.get("API_KEY_KREATIVE_LABS")
import os
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from benkizapi.models import Transaction

api_key = os.environ.get("API_KEY_KREATIVE_LABS")


################################
# COMPLETE PURCHASE VIEW
################################


@login_required(login_url='login')
def completepurchase(request):

    if request.method != "POST":
        return redirect("checkout")

    user = request.user
    profile = UserProfile.objects.get(user=user)
    cart = Cart.objects.get(user=user)

    cart.calcTotal
    amount = int(cart.totalcost)

    if amount <= 1:
        return HttpResponse("Invalid amount")

    external_reference = f"order_{user.id}_{datetime.now().timestamp()}"

    transaction = Transaction.objects.create(
        user=user,
        customerName=user.username,
        phone_number=profile.phone_number,
        amount=amount,
        status="PENDING",
        external_reference=external_reference
    )

    payload = {
        "phone_number": profile.phone_number,
        "amount": amount,
        "callback_url": "https://safariocom.pythonanywhere.com/api/handle_payment_callback/",
        "external_reference": external_reference,
        "metadata": {
            "order_id": str(transaction.id),
            "customer_name": user.username,
        },
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://lipia-api.kreativelabske.com/api/v2/payments/stk-push",
        headers=headers,
        json=payload,
        timeout=30
    )

    result = response.json()

    if result.get("success"):
        transaction.transaction_reference = result["data"]["TransactionReference"]
        transaction.message = result.get("customerMessage")
        transaction.save()

        return redirect("payment_waiting", reference=transaction.transaction_reference)

    transaction.status = "FAILED"
    transaction.save()

    return HttpResponse("Failed to initiate payment.")



@login_required(login_url='login')
def paymentWaiting(request, reference):

    transaction = Transaction.objects.filter(
        transaction_reference=reference
    ).first()

    if not transaction:
        return HttpResponse("Invalid transaction reference.")

    return render(request, "payment_waiting.html", {
        "reference": reference,
        "transaction": transaction
    })

################################ end payment process ################################


# Create your views here.
def createcontext(request=None):
    context = {}
    lessons = Lesson.objects.all()
    items = Item.objects.order_by('-id')
    courses = Lesson.objects.all()
    heros = HeroBanner.objects.all()

    if request is not None:
        if CourseBasket.objects.filter(user = request.user).exists():
            coursebasket = CourseBasket.objects.get(user = request.user)
        else:
            CourseBasket.objects.create(user=request.user)
            coursebasket = CourseBasket.objects.get(user = request.user)
        selectedCourses = coursebasket.lessons_selected.all()

        cart = Cart.objects.filter(user = request.user).exists()
        if cart :
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.create(user = request.user)
        numberofcartitems = 0

        if UserProfile.objects.filter(user = request.user).exists():
            profile = UserProfile.objects.get(user = request.user)
        else:
            profile = UserProfile.objects.create(user=request.user)
        cartitems = CartItem.objects.filter(cart = cart)
        profiles = UserProfile.objects.all()
        for cartItem in cartitems:
            numberofcartitems += cartItem.quantity
        blogposts = BlogPost.objects.all()
        cartitemscount = len(cartitems)

        wishlistexists = WishList.objects.filter(user=request.user).exists()
        
        if wishlistexists:
            wishlist = WishList.objects.get(user=request.user)
            wishitems = WishItem.objects.filter(wishlist = wishlist)
                

            for item in items:
                if int(len(wishitems)) == 0:
                    item.is_wished = False
                    item.save()
                for wishitem in wishitems:
                    if wishitem.item.name == item.name:
                        item.is_wished = True
                        item.save()
                        wishitem.save()
                        wishlist.save()
            context = context|{'wishlist':wishlist,'wishitems':wishitems,'coursebasket':coursebasket,'selectedCourses':selectedCourses}
            
        else:
            wishlist = WishList.objects.create(user = request.user)
            wishitems = WishItem.objects.filter(wishlist = wishlist)
            context = context|{'wishlist':wishlist,'wishitems':wishitems}
            
        usersocialsexists = Social.objects.filter(user = request.user).exists()
        if usersocialsexists is False:
            usersocials = Social.objects.create(user=request.user)
        else:
            usersocials = Social.objects.get(user=request.user)
        
        context1 = {
                    'cart':cart,
                    'cartitems':cartitems,
                    'blogposts':blogposts,
                    'cartitemscount':cartitemscount,
                    'profile':profile,
                    'profiles':profiles,
                    'usersocials':usersocials,
                    'numberofcartitems':numberofcartitems
                   
                    }
        context = context|context1
    socials = Social.objects.all()
    team = UserProfile.objects.filter(is_team = True)
    blogposts = BlogPost.objects.all()

    comments = Comment.objects.all()


    locations = Location.objects.all()

    context = context|{'items':items,'team':team,'socials':socials,'blogposts':blogposts,
                       'lessons':lessons,'comments':comments,'locations':locations, 'heros':heros}
    return context

def rendercontexttemplate(request,templatename):
    if request.user.username == '':
        context = createcontext()
        return render(request,f'{templatename}.html',context)
    else:
        context = createcontext(request)
        return render(request,f'{templatename}.html',context)

categorynavlist = []
def landing(request):
    if request.user.username == '':
        return render(request,'main.html')
    else:
        user = request.user
        profile = UserProfile.objects.filter(user = user).exists()

        if profile is None:
            newprofile = UserProfile.objects.create(user = user)
            newprofile.save()
            return redirect('login')
        cart = Cart.objects.filter(user = user).exists()
        if cart:
            pass
        else:
            auth.logout
            return redirect('login')
        return rendercontexttemplate(request,'main')

def home(request):
    return rendercontexttemplate(request,'main')
@login_required(login_url='login')
def profile(request):
    return rendercontexttemplate(request,'profile')


class ShopView(generic.ListView):
    model = Item
    template_name = 'shop.html'
    queryset = Item.objects.all()
    context_object_name = 'things'
    paginate_by = 8

    def get_queryset(self):
        return Item.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if self.request.user.username != '':
            context.update(createcontext(self.request))
        else:
            context.update(createcontext())
        return context

def searchitem(request):
    query = request.GET.get('query')
    prevpage = request.META.get('HTTP_REFERER')
    if query == "":
        messages.info(request,'Please type something')
        return redirect(prevpage)
    if query:
        stuff = Item.objects.filter(
        Q(name__icontains=query)|
        Q(description__icontains=query)|
        Q(additionalinfo__icontains=query)|
        Q(price__icontains=query)|
        Q(category__icontains=query)
        ).order_by('name')
        
        if stuff.__len__() < 1:
            stuff = Item.objects.all()
            messages.info(request,'Sorry No such item !')
    else:
        stuff = Item.objects.all().order_by('name')
    page = request.GET.get('page',1)
    paginator = Paginator(stuff,8)

    try:
        somestuff = paginator.page(page)
    except PageNotAnInteger:
        somestuff=paginator.page(1)
    except EmptyPage:
        somestuff = paginator.page(paginator.num_pages)

    context = {}
    if request.user.is_authenticated:
        context = createcontext(request)

    else:
        context = createcontext()
    cont2 = {'stuff':somestuff}
    context = context|cont2


    return render(request,'searchpage.html',context)

@login_required
def updatecart(request):
    prevpage = request.META.get('HTTP_REFERER')
    return redirect(prevpage)

def productdetails(request,itemid):

    item = Item.objects.get(id=itemid)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user = request.user)
        cartitems = CartItem.objects.filter(cart = cart)

        for cartitem in cartitems:
            if cartitem.item == item:
                item = cartitem

        cartitemslist = list(cartitems.values())
    category = item.category
    relateditems = Item.objects.filter(category = category)
    item.numberofviews += 1
    item.save()

    allitems = list(Item.objects.values())
    if request.user.is_authenticated:
        context2 = {'item':item,"cartitemslist":cartitemslist,'relateditems':relateditems}
    else:
        context2 = {'item':item,'relateditems':relateditems}

    if request.user.username != '':
        context = createcontext(request)
        context = context|context2
    else:
        context = createcontext(request=None)
        context = context|context2
        
    return render(request,'productdetails.html',context)
@login_required(login_url = 'login')
def shoppingcart(request):
    return rendercontexttemplate(request,'shoppingcart')

@login_required(login_url = 'login',)
def checkout(request):
    context = createcontext(request)
    return render(request,'checkout.html',context)

@login_required(login_url='login')
def wishlist(request):
    return rendercontexttemplate(request,'wishlist')

@login_required(login_url='login')
def addToWishlist(request,id):
    prevpage = request.META.get('HTTP_REFERER')
    item = Item.objects.get(id = id)
    user = auth.get_user(request)
    #  check existance
    if WishList.objects.filter(user = user).exists():
        wishlist = WishList.objects.get(user = user)
        if WishItem.objects.filter(item = item).exists():
            pass
        else:
            wishitem = WishItem.objects.create(item = item)
            wishitem.wishlist = wishlist
            wishitem.save()
            wishlist.save()
        return redirect(prevpage)
    else:
        WishList.objects.create(user = user)
        return redirect(prevpage)

def blogdetails(request):
    return rendercontexttemplate(request,'blogdetails')

def blog(request):
    blogposts = BlogPost.objects.all()
    context ={}
    if request.user.username != '':
        context = createcontext(request)
    else:
        context = createcontext()

    context = context|{'blogpostposts':blogposts}
    return render(request,'blog.html',context)


@login_required(login_url='login')
def postblog(request):
    if request.method =='POST':
        title = request.POST.get('blogtitle')
        content = request.POST.get('blogcontent')
        thumbnail = request.FILES.get('cover_pic')

        if BlogPost.objects.filter(title = title).exists():
            messages.info(request,'Title has already been used !')
            return redirect('createblog')
        else:
            BlogPost.objects.create(title = title,content = content,coverimage = thumbnail,user = request.user)


    return rendercontexttemplate(request,'blog')

@login_required(login_url='login')
def createblog(request):
    return render(request,'createblog.html')

def readblog(request,id):
    blogpost = BlogPost.objects.get(id=id)
    user = auth.get_user(request)
    view_exists = View.objects.filter(user = user).exists()
    if view_exists:
        print('YOu have already viewed !')
    else:
        newview = View.objects.create(user = user,blogpost = blogpost)
        newview.save()
    viewcount = len(View.objects.filter(blogpost = blogpost))
    blogpost.numberofviews = viewcount
    blogpost.save()
    context = createcontext(request)
    context = context|{'views':viewcount,'post':blogpost}
    return render(request,'readblog.html',context)

def messageus(request,userid):
    if request.POST:

        message = request.POST.get('message')
        if userid == 'anonymous':
            newmess=Message.objects.create(user = None,body=message)
            newmess.save()
        else:
            user = User.objects.get(id = userid)
            newmess = Message.objects.create(user = user,body=message)
            newmess.save()
            messages.info(request,'Message sent !')

    return render(request,'contact.html')


@login_required(login_url='login')
def removewishitem(request,pk):
    wishlist = WishList.objects.get(user = request.user)
    
    prevpage = request.META.get('HTTP_REFERER')
    
    
    itemtodelete = Item.objects.get(id=pk)
    wishitems = WishItem.objects.filter(wishlist = wishlist)
    for wishitem in wishitems:
        if wishitem.item == itemtodelete:
            wishitem.item.is_wished = False
            wishitem.item.save()
            wishitem.delete()
            
    return redirect(prevpage)
    

@login_required(login_url='login')
def removecartitem(request,pk):
    cart = Cart.objects.get(user = auth.get_user(request))
    cartitems= CartItem.objects.filter(cart = cart)

    for item in cartitems:
        if CartItem.objects.get(id=pk):
            CartItem.objects.get(id=pk).delete()
            return redirect('shoppingcart')
    else:
        print('There is no such object in the cart !!!')
        return redirect('shoppingcart')

def Class(request,pk):
    if request.user.is_authenticated:
        context = createcontext(request)
        courseBasket = CourseBasket.objects.get(user = request.user)
        lessons_selected = courseBasket.lessons_selected.all()
        lessons_enrolled = courseBasket.lessons_enrolled.all()

        context = context|{"lessons_selected":lessons_selected,"lessons_enrolled":lessons_enrolled}
    else:
        context = createcontext()
    if request.method == 'POST':
        if str(pk) != 'menu':
            lesson = Lesson.objects.get(id=pk)
            coursebasket = CourseBasket.objects.get(user=request.user)
            lesson.coursebasket = coursebasket
            lesson.save()
            return redirect('course-basket')
        else:
            return render(request,'class.html',context)
        
    return render(request,'class.html',context)

def contact(request):
    return rendercontexttemplate(request,'contact')

def gallery(request):
    if auth.user_logged_in:
        return rendercontexttemplate(request,'cakegallery')
    else:
        items = Item.objects.all()
        cont = createcontext()
        cont2 = cont|{'things':items}
    return render('cakegallery.html',cont2)


# actions

def register(request):
    if request.POST:
        username = request.POST.get('regusername')
        password1 = request.POST.get('regpassword1')
        password2 = request.POST.get('regpassword2')
        email = request.POST.get('regemail')

        if password1 ==password2:
            if User.objects.filter(email = email).exists():
                messages.info(request,'Email already exists !!')
                return redirect('login')
            elif User.objects.filter(username = username).exists():
                messages.info(request,'Username already taken !!')
                return redirect('login')
            else:
                newuser = User.objects.create_user(username=username,password=password1,email=email)
                profile = UserProfile.objects.create(user = newuser)
                profile.save()
                usser = User.objects.get(username = username)

                Cart.objects.create(user = usser)
                WishList.objects.create(user = usser)
                return redirect('login')
        else:
            messages.info(request,"Passwords don't match !!")
            return redirect('login')

    return render(request,'login2.html')




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
            return redirect(prevPage(request))
    else:
        context = createcontext(request)
        context = {
            'form':form,
        } | context


        return render(request,'updateprofile.html',context)
def login(request):
    if request.method =='POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=name,password=password)
        if user is not None:
            person = User.objects.get(username=name)
            profile_present = UserProfile.objects.filter(user=person).exists()
            if profile_present:
                profile = UserProfile.objects.get(user=person)
                auth.login(request,user)
                if profile.lastname and profile.phone_number :
                    pass
                else:
                    return redirect('updateprofile')
                user = auth.get_user(request)

                return redirect('home')
            else:
                newprofile = UserProfile.objects.create(user=person)
                newprofile.save()
                auth.login(request,user)
                user = auth.get_user(request)
                return redirect('updateprofile')                
        else:
            messages.info(request,f"Wrong credentials for **{name.upper()}** .")
            return redirect('login')
    else:
        return rendercontexttemplate(request,templatename='login2')


@login_required(login_url='login')
def accessAdminPanel(request,page):
    context = createcontext(request)

    if page != 'menu':
        return render(request,f'admin/{page}.html',context)
    else:
        return render(request,'admin/admin.html',context)
    

def supersu(request):
    return redirect('/admin')
@login_required(login_url='login')
def admin(request):
    context = createcontext(request)
    return render(request,'admin/admin.html',context)
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='login')
def buyItem(request,pk):
    user = auth.get_user(request)
    cart = Cart.objects.get(user = user)
    
    prevpage = request.META.get('HTTP_REFERER')
        
    item = Item.objects.get(id = pk)
    item.numberOfItems -=1
    item.soldUnits +=1
    cart_item = CartItem.objects.filter(cart = cart,item=item).exists()
    if cart_item :
        cart_item = CartItem.objects.get(cart = cart,item = item)
    else:
        cart_item = CartItem.objects.create(cart = cart,item = item)

    
    cart_item.quantity +=1
    cart_item.save()
    cart.calcTotal
    item.save()
    cart.save()

    return redirect(prevpage)

@login_required(login_url='login')
def createcomment(request):
    user = request.user
    profile = UserProfile.objects.get(user = user)
    if request.method == "POST":
        body = request.POST.get('textbody')
        if body:
            newcomment = Comment.objects.create(user = user,profile=profile,body=body)
            newcomment.save()
            return redirect('home')
        else:
            messages.info(request,'You did not comment !')
            return redirect('createcomment')
    context = createcontext(request)

    return render(request,'createcomment.html',context)

def rate(request,star_no):
    rate_exist = Rating.objects.filter(user = request.user).exists()
    if rate_exist:
        rating = Rating.objects.get(user = auth.get_user(request))
        rating.stars = star_no
        rating.save()
        
    else:
        rating = Rating.objects.create(user = auth.get_user(request))
        rating.stars = star_no
        rating.save()
    messages.info(request,'Thanks for rating us !')

    return redirect('home')

@login_required(login_url='login')
def additem(request):
    if request.method == 'POST':
        name = request.POST.get('itemName')
        description = request.POST.get('itemDescription')
        thumbnail = request.FILES.get('itemThumbnail')
        price = request.POST.get('itemPrice')
        additionalinfo = request.POST.get('additionalinfo')
        numberOfItems = request.POST.get('numberOfItems')
        category = request.POST.get('cakeCategory')
        
        newitem = Item.objects.create(name=name,category=category,numberOfItems=numberOfItems,description=description,price=price,additionalinfo=additionalinfo,thumbnail=thumbnail)
        newitem.save()
        messages.info(request,f'{name} saved successfully 😊') 
        return redirect('/adminpanel/itemmanager')  
    else:
        return redirect('/adminpanel/menu')
@login_required(login_url='login')
def deleteitem(request,id):
    localhost = 'http://127.0.0.1:8000'
    pythonanywhere = 'https://safariocom.pythonanywhere.com'
    url = localhost + f'/api/get/{id}'
    
    response = requests.delete(url)
    print('status code : ' + str(response.status_code))
    # print(response.json(),safe=False)
    print(response.text)
    print(response.url)
    print(response.headers)
    print(response.content)
    print(response.request)
    print(response.cookies)

    return redirect('/adminpanel/itemmanager')
    
@login_required(login_url='login')
def modifyitem(request,id):
    
    if request.method == 'POST':
        localhost = 'http://127.0.0.1:8000'
        pythonanywhere = 'https://safariocom.pythonanywhere.com'
        url = f'http://127.0.0.1:8000/api/get/{id}'
        
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        itemadditionalinfo = request.POST.get('additionalinfo')
        numberofitems = request.POST.get('number')
        category = request.POST.get('itemcategory')
        
        
        headers = {
                    "Content-Type":"application/json"
                    
                }
        body = {
            "name": f"{name}",
            "description": f"{description}",
            "price": f"{price}",
            "numberOfItems": numberofitems,
            "category": f"{category}"
        }
        
        try:
            response = requests.patch(url,headers=headers,json=body)
            try:
                response = JsonResponse({
                    "status_code":response.status_code,
                    "response":response.json()
                })
                return redirect(urls.reverse())
            except:
                return redirect("/adminpanel/itemmanager")
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error':str(e)},status=500,safe=False)
            # return HttpResponseRedirect(redirect_to='/home')
        
def updatesocials(request,id):
    if request.method == 'POST':
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        youtube = request.POST.get('youtube')
        
        social_to_update = Social.objects.get(user = request.user)
        
        print(f"""
              
              facebook : {facebook}
              instagram : {facebook}
              twitter : {twitter}
              youtube : {youtube}
              
              """)
        
        if facebook != '':
            social_to_update.facebook = facebook
        else:
            social_to_update.facebook = None
            
        if instagram != '':
            social_to_update.instagram = instagram
        else:
            social_to_update.instagram = None
        if twitter != '':
            social_to_update.twitter = twitter
        else:
            social_to_update.twitter = None
        if youtube != '':
            social_to_update.youtube = youtube
        else:
            social_to_update.youtube = None
        
        social_to_update.save()
        return redirect(prevPage(request))
    return redirect('updateprofile')
            
def classSignup(request):
    if request.method == 'POST':
        learnerprofiles = LearnerProfile.objects.all()
        prevpage = request.META.get('HTTP_REFERER')
        name = request.POST.get('studentname')
        phone_number = request.POST.get('phone_number')
        phone = int(phone_number)
        mode_of_study = request.POST.get('mode_of_study')
        email = request.POST.get('email')
        
        if mode_of_study == 'select':
            messages.info(request,"Please Choose a mode of study !")
            return redirect(prevpage)
        else:
            for learnerprofile in learnerprofiles:
                if (int(learnerprofile.phone) == phone) or (learnerprofile.email == email):
                    if int(learnerprofile.phone) == phone:
                        messages.info(request,f'{phone_number} has already been taken !')
                    elif learnerprofile.email == email:
                        messages.info(request,f'{email} has already been taken !')
                else:
                    new_learner = LearnerProfile.objects.create(name = name,phone = phone_number,mode_of_learning = mode_of_study,email = email)
                    new_learner.save()
                    
        
    return redirect(prevpage)

@login_required(login_url='login')
def takeCourse(request,courseid):
    prevpage = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        coursebasket = CourseBasket.objects.get(user = request.user)
        lesson = Lesson.objects.get(id = courseid)
        coursebasket.lessons_selected.add(lesson)
        registeredcourses = CourseBasket.objects.filter(user = request.user)

            
    return redirect(prevpage)

@login_required(login_url='login')
def courseBasket(request):
    user = request.user
    
    if LearnerProfile.objects.filter(user=request.user).exists():
        coursebasket = CourseBasket.objects.filter(user = user)
    else:
        LearnerProfile.objects.create(user=request.user,name=request.user.username)
        coursebasket = CourseBasket.objects.filter(user = user)
        
        
    if user.is_authenticated:
        context = createcontext(request)
    else:
        context = createcontext()
    
    return render(request,'coursebasket.html',context)

@login_required(login_url='login')
def unselectCourse(request,courseid):
    prevpage = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        coursetounselect = Lesson.objects.get(id = courseid)
        courseBasket = CourseBasket.objects.get(user = request.user)
        print(f" ------------------>  courses selected               {courseBasket.lessons_selected.all()} and course to delete                       {coursetounselect}")
        courseBasket.lessons_selected.remove(coursetounselect)
    return redirect(prevpage)


@login_required(login_url='login')
def subscribeCourse(request,courseid):
    if request.method == 'POST':
        course = Lesson.objects.get(id=courseid)
        courseBasket = CourseBasket.objects.get(user = request.user)
        courseBasket.lessons_enrolled.add(course)
        courseBasket.lessons_selected.remove(course)
        course_price = course.price
        phone_number = LearnerProfile.objects.get(user = request.user).phone

        if phone_number is None:
            if UserProfile.objects.get(user = request.user).phone_number is not None:
                phone_numberr = UserProfile.objects.get(user = request.user).phone_number
                LearnerProfile.objects.get(user = request.user).phone = phone_numberr
                return redirect('course-basket')
            else:
                messages.info(request,'Please update your phone number !')
                return redirect('updateprofile')
    
        messages.info(request,'Subscribed successfully')
    messages.info(request,'Login first !')
    return redirect(prevPage(request))

@login_required(login_url='login')
def unsubscribeCourse(request,courseid):
    return redirect(prevPage(request))

def prevPage(request):
    prevpage = request.META.get('HTTP_REFERER')
    return prevpage


@login_required(login_url='login')
def check_payment_status(request, reference):
    """
    Fetch payment status directly from Lipia API using the transaction reference.
    """
    # api_key = api_key 
    # Store your API key in settings or .env
    base_url = "https://lipia-api.kreativelabske.com/api/v2"

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.get(
            f"{base_url}/payments/status",
            headers=headers,
            params={"reference": str(reference)},
            timeout=60
        )
        result = response.json()
        print (f'''
        
        
{result}


''')

        # Default empty response if missing fields
        payment_data = result.get("data", {}).get("response", {})

        # Prepare a consistent JSON structure for frontend
        data = {
            "Status": payment_data.get("Status", "UNKNOWN"),
            "ResultCode": payment_data.get("ResultCode", 0),
            "ResultDesc": payment_data.get("ResultDesc", ""),
            "MpesaReceiptNumber": payment_data.get("MpesaReceiptNumber", ""),
            "message": result.get("customerMessage", result.get("message", "")),
        }

        return JsonResponse(data)

    except requests.exceptions.RequestException as e:
        # Network or API error
        return JsonResponse({
            "Status": "ERROR",
            "ResultCode": -1,
            "ResultDesc": str(e),
            "MpesaReceiptNumber": "",
            "message": "Error fetching payment status."
        }, status=500)

def thanks(request):
    return render (request,'thanks.html')