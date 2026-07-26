from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework_simplejwt.tokens import RefreshToken

from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.db.models import Q
import json

from .serializers import *
from main.models import *
from .models import *


from django.http import JsonResponse
import os



# ─────────────────────────────────────────────
# LEGACY ENDPOINTS (kept for compatibility)
# ─────────────────────────────────────────────

@api_view(['GET'])
def getAllItems(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PATCH', 'PUT'])
def getItem(request, id):
    try:
        item = Item.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def getCartItem(request, id):
    cart = Cart.objects.get(user=request.user)
    try:
        cartitem = CartItem.objects.get(cart=cart, id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CartItemSerializer(cartitem)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CartItemSerializer(cartitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        cartitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_all_items(request):
    allitems = Item.objects.all()
    if not request.user.is_superuser:
        return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
    allitems.delete()
    return Response({'status': 'All data deleted.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_user(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return Response({'status': 'No such User'}, status=status.HTTP_200_OK)
    operator = request.user
    operatorprofile = UserProfile.objects.get(user=operator)
    if request.method == 'DELETE':
        if operatorprofile.is_normal_admin:
            user.delete()
            return Response({'status': 'User deleted.'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': "You dont have clearance !"}, status=status.HTTP_200_OK)
    else:
        return Response({'status': "Bad request !"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def handle_payment_callback(request):
    data = request.data
    result = data.get("response", {})
    external_reference = result.get("ExternalReference")
    transaction = Transaction.objects.filter(external_reference=external_reference).first()
    if not transaction:
        return HttpResponse("ok", status=200, content_type="text/plain")
    if transaction.status == "SUCCESS":
        return HttpResponse("ok", status=200, content_type="text/plain")
    transaction.callback_body = json.dumps(data)
    status_value = result.get("Status")
    if status_value == "Success":
        transaction.status = "SUCCESS"
        transaction.status_bool = True
    else:
        transaction.status = "FAILED"
        transaction.status_bool = False
    transaction.mpesaReceiptNumber = result.get("MpesaReceiptNumber")
    transaction.responseDescription = result.get("ResultDesc")
    transaction.merchantRequestID = result.get("MerchantRequestID")
    transaction.save()
    return HttpResponse("ok", status=200, content_type="text/plain")


# ─────────────────────────────────────────────
# NEW REACT API ENDPOINTS
# ─────────────────────────────────────────────

# ── AUTH ──
@api_view(['GET'])
@ensure_csrf_cookie
def csrf_token_view(request):
    return Response({
        "success": True
    })


# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
# -------------------------------------------------
# CSRF TOKEN
# -------------------------------------------------

@api_view(["GET"])
@ensure_csrf_cookie
def csrf_token_view(request):
    return Response({
        "success": True
    })


# -------------------------------------------------
# COOKIE SETTINGS
# Uses values from settings.py
# -------------------------------------------------

# def cookie_options(max_age):

#     return {
#         "httponly": settings.SESSION_COOKIE_HTTPONLY,
#         "secure": settings.SESSION_COOKIE_SECURE,
#         "samesite": settings.SESSION_COOKIE_SAMESITE,
#         "path": settings.SESSION_COOKIE_PATH,
#         "max_age": max_age,
#     }


def cookie_options(max_age):
    return {
        "httponly": True,
        "secure": True,
        "samesite": "None",
        "path": "/",
        "max_age": max_age,
    }

# -------------------------------------------------
# SET TOKENS
# -------------------------------------------------

def set_tokens(response, user):

    refresh = RefreshToken.for_user(user)

    response.set_cookie(
        key="access_token",
        value=str(refresh.access_token),
        **cookie_options(900)
    )

    response.set_cookie(
        key="refresh_token",
        value=str(refresh),
        **cookie_options(604800)
    )

    return response


# -------------------------------------------------
# LOGIN
# -------------------------------------------------

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):

    user = auth.authenticate(
        username=request.data.get("username"),
        password=request.data.get("password")
    )


    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    role = "CUSTOMER"
    if user.is_superuser:
        role = "SUPER_ADMIN"
    elif user.is_staff:
        role = "ADMIN"

    userdata = UserSerializer(user).data
    userdata = userdata | {"role":role}

     

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": userdata
    })

# -------------------------------------------------
# REFRESH
# -------------------------------------------------

@api_view(["POST"])
@permission_classes([AllowAny])
def refresh(request):

    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response(
            {"error": "No refresh token provided"},
            status=401
        )

    try:
        refresh_obj = RefreshToken(refresh_token)
    except Exception:
        return Response(
            {"error": "Invalid refresh token"},
            status=401
        )

    return Response({
        "access": str(refresh_obj.access_token)
    })


# -------------------------------------------------
# LOGOUT
# -------------------------------------------------

@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):

    response = Response({
        "success": True
    })

    response.delete_cookie(
        "access_token",
        path=settings.SESSION_COOKIE_PATH
    )

    response.delete_cookie(
        "refresh_token",
        path=settings.SESSION_COOKIE_PATH
    )

    return response


# -------------------------------------------------
# REGISTER
# -------------------------------------------------

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):

    username = request.data.get(
        "username",
        ""
    ).strip()

    password = request.data.get(
        "auth",
        ""
    ).strip()

    email = request.data.get(
        "email",
        ""
    ).strip()

    lastname = request.data.get(
        "lastname",
        ""
    ).strip()

    if not username or not password:

        return Response(
            {
                "error":
                "Username and password are required"
            },
            status=400
        )

    if User.objects.filter(
        username=username
    ).exists():

        return Response(
            {
                "error":
                "Username already exists"
            },
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )

    profile = UserProfile.objects.create(
        user=user,
        lastname=lastname
    )

    Cart.objects.create(
        user=user
    )

    WishList.objects.create(
        user=user
    )

    CourseBasket.objects.create(
        user=user
    )

    return Response(
        {"message":"success"
        },
        status=201
    )


# -------------------------------------------------
# CURRENT USER
# -------------------------------------------------



@api_view(["GET"])
def me_view(request):
    user = request.user
    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    role = "CUSTOMER"
    if user.is_superuser:
        role = "SUPER_ADMIN"
    elif user.is_staff:
        role = "ADMIN"

    userdata = UserSerializer(user).data
    userdata = userdata | {"role":role}

    refresh = RefreshToken.for_user(user)
    profile = UserProfile.objects.filter(user=request.user).first()

    return Response({
        "user": userdata,
        "profile": UserProfileSerializer(profile).data if profile else None

    })


# ── ITEMS ──

from django.db.models import Q

@api_view(['GET'])
@permission_classes([AllowAny])
def items_list(request):
    queryset = Item.objects.all().order_by('-id')

    search = request.GET.get('search', '').strip().lower()
    category = request.GET.get('category', '').strip().lower()
    limit = request.GET.get('limit', None)

    # SEARCH (fixed for ManyToMany)
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(additionalinfo__icontains=search) |
            Q(category__name__icontains=search)
        ).distinct()

    # CATEGORY FILTER (FIXED)
    if category and category != 'all':
        queryset = queryset.filter(
            Q(category__name__iexact=category) |
            Q(category__name__icontains=category)
        ).distinct()

    # LIMIT
    if limit:
        try:
            queryset = queryset[:int(limit)]
        except (ValueError, TypeError):
            pass

    serializer = ItemSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def item_detail(request, id):
    try:
        item = Item.objects.get(id=id)
        item.numberofviews = (item.numberofviews or 0) + 1
        item.save(update_fields=['numberofviews'])
    except Item.DoesNotExist:
        return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(ItemSerializer(item).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def items_featured(request):
    items = Item.objects.order_by('-numberofviews', '-id')[:8]
    return Response(ItemSerializer(items, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def categories_list(request):
    from main.models import cakecategories
    return Response([{'value': c[0], 'label': c[1]} for c in cakecategories])


# ── CART ──

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def cart_response(user):
    cart = get_or_create_cart(user)
    cart.calcTotal
    items = CartItem.objects.filter(cart=cart).select_related('item')
    return Response({
        'cart': CartSerializer(cart).data,
        'items': CartItemDetailSerializer(items, many=True).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_view(request):
    return cart_response(request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart_add(request):
    item_id = request.data.get('item_id')
    quantity = int(request.data.get('quantity', 1))
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

    cart = get_or_create_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    cart.calcTotal
    return cart_response(request.user)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_item_view(request, id):
    cart = get_or_create_cart(request.user)
    try:
        cart_item = CartItem.objects.get(id=id, cart=cart)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        quantity = int(request.data.get('quantity', 1))
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
    elif request.method == 'DELETE':
        cart_item.delete()

    cart.calcTotal
    return cart_response(request.user)


# ── WISHLIST ──

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wishlist_view(request):
    wishlist, _ = WishList.objects.get_or_create(user=request.user)
    items = WishItem.objects.filter(wishlist=wishlist).select_related('item')
    return Response(WishItemSerializer(items, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wishlist_add(request):
    item_id = request.data.get('item_id')
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
    wishlist, _ = WishList.objects.get_or_create(user=request.user)
    WishItem.objects.get_or_create(wishlist=wishlist, item=item)
    return Response({'status': 'added'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def wishlist_remove(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        wishlist = WishList.objects.get(user=request.user)
        WishItem.objects.filter(wishlist=wishlist, item=item).delete()
    except:
        pass
    return Response({'status': 'removed'})


# ── LESSONS / CLASSES ──

@api_view(['GET'])
@permission_classes([AllowAny])
def lessons_list(request):
    lessons = Lesson.objects.filter(availability=True)
    return Response(LessonSerializer(lessons, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lesson_enroll(request, id):
    try:
        lesson = Lesson.objects.get(id=id)
    except Lesson.DoesNotExist:
        return Response({'error': 'Lesson not found.'}, status=status.HTTP_404_NOT_FOUND)
    basket, _ = CourseBasket.objects.get_or_create(user=request.user)
    basket.lessons_selected.add(lesson)
    return Response({'status': 'selected'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def lesson_unenroll(request, id):
    try:
        lesson = Lesson.objects.get(id=id)
        basket, _ = CourseBasket.objects.get_or_create(user=request.user)
        basket.lessons_selected.remove(lesson)
    except:
        pass
    return Response({'status': 'removed'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_basket(request):
    basket, _ = CourseBasket.objects.get_or_create(user=request.user)
    return Response({
        'selected': LessonSerializer(basket.lessons_selected.all(), many=True).data,
        'enrolled': LessonSerializer(basket.lessons_enrolled.all(), many=True).data,
    })


# ── PROFILE ──

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'GET':
        return Response(UserProfileSerializer(profile).data)
    elif request.method == 'PATCH':
        allowed = ['lastname', 'phone_number', 'country', 'county', 'address_or_street', 'apartment_or_house_name_or_number']
        for field in allowed:
            if field in request.data:
                setattr(profile, field, request.data[field])
        profile.save()
        return Response(UserProfileSerializer(profile).data)


# ── TESTIMONIALS ──

@api_view(['GET'])
@permission_classes([AllowAny])
def testimonials_list(request):
    comments = Comment.objects.select_related('user', 'profile', 'rating').all()
    return Response(CommentSerializer(comments, many=True).data)


# ── TEAM ──

@api_view(['GET'])
@permission_classes([AllowAny])
def team_list(request):
    team = UserProfile.objects.filter(is_team=True)
    return Response(TeamMemberSerializer(team, many=True).data)


# ── LOCATIONS ──

@api_view(['GET'])
@permission_classes([AllowAny])
def locations_list(request):
    locations = Location.objects.all()
    return Response(LocationSerializer(locations, many=True).data)


# ── CONTACT ──

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contact_send(request):
    body = request.data.get('message', '').strip()
    if not body:
        return Response({'error': 'Message cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)
    Message.objects.create(user=request.user, body=body)
    return Response({'status': 'Message sent.'})


# ── CHECKOUT ──

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_view(request):
    from django.shortcuts import redirect
    import os
    import requests as req

    cart = get_or_create_cart(request.user)
    cart.calcTotal
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    phone = profile.phone_number or '0700000000'
    phone = phone.replace('+', '').replace(' ', '').replace('-', '')
    if phone.startswith('0'):
        phone = '254' + phone[1:]

    amount = float(cart.totalcost) if hasattr(cart, 'totalcost') and cart.totalcost else 1.0
    amount = max(round(amount), 1)

    API_KEY = os.environ.get('API_KEY_KREATIVE_LABS', '')

    transaction = Transaction.objects.create(
        user=request.user,
        customerName=request.user.username,
        phone_number=phone,
        amount=amount,
        status='PENDING',
    )

    if not API_KEY:
        transaction.status = 'PENDING'
        transaction.transaction_reference = f'TEST-{transaction.id}'
        transaction.save()
        # Clear cart
        cart_items.delete()
        cart.calcTotal
        return Response({'reference': transaction.transaction_reference, 'status': 'PENDING'})

    headers = {'Content-Type': 'application/json', 'x-api-key': API_KEY}
    payload = {
        'phone': phone,
        'amount': amount,
        'account_name': 'Benkiz Bakers',
        'account_number': 'BENKIZ001',
        'narrative': f'Order by {request.user.username}',
    }

    try:
        response = req.post(
            'https://api.kreativelabs.ke/v1/payments/stk-push',
            headers=headers,
            json=payload,
            timeout=30
        )
        result = response.json()
        if result.get('success'):
            transaction.transaction_reference = result['data'].get('TransactionReference', f'TXN-{transaction.id}')
            transaction.message = result.get('customerMessage', '')
            transaction.save()
        else:
            transaction.status = 'FAILED'
            transaction.save()
            return Response({'error': 'Payment initiation failed.'}, status=status.HTTP_502_BAD_GATEWAY)
    except Exception as e:
        transaction.status = 'FAILED'
        transaction.save()
        return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

    cart_items.delete()
    cart.calcTotal
    return Response({'reference': transaction.transaction_reference, 'status': 'PENDING'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_status(request, reference):
    transaction = Transaction.objects.filter(transaction_reference=reference, user=request.user).first()
    if not transaction:
        return Response({'error': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'status': transaction.status, 'reference': reference})


# ── HERO BANNERS ──

@api_view(['GET'])
@permission_classes([AllowAny])
def hero_banners(request):
    heros = HeroBanner.objects.all()
    return Response(HeroBannerSerializer(heros, many=True).data)

    
# ── TEAM ──

@api_view(['GET'])
@permission_classes([AllowAny])
def team(request):
    return Response([])
    

# ── TESTIMONIALS ──

@api_view(['GET'])
@permission_classes([AllowAny])
def testimonials(request):
    return Response([])
    


# ── STATS ──

@api_view(['GET'])
@permission_classes([AllowAny])
def stats_view(request):
    return Response({
        'products': Item.objects.count(),
        'lessons': Lesson.objects.count(),
        'team': UserProfile.objects.filter(is_team=True).count(),
        'locations': Location.objects.count(),
    })





