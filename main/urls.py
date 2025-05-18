from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('completepurchase/',views.completepurchase,name='completepurchase'),

    path('profile',views.profile,name='profile'),
    path('shop/',views.shop,name='shop'),
    path('shopdetails/',views.shopdetails,name='shopdetails'),
    path('shoppingcart/',views.shoppingcart,name='shoppingcart'),
    path('checkout/',views.checkout,name='checkout'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('Class/',views.Class,name='Class'),
    path('buyItem/<str:pk>',views.buyItem,name='buyItem'),
    path('blogdetails/',views.blogdetails,name='blogdetails'),
    path('blog/',views.blog,name='blog'),
    path('contact/',views.contact,name='contact'),
    path('gallery/',views.gallery,name='gallery'),
    path('register/',views.register,name='register'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    
    
    

    path('api/payment/callback/', views.payment_callback, name='payment_callback'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


