from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('super-su/',views.supersu,name='super-su'),
    path('adminpanel/<str:page>',views.accessAdminPanel,name='adminpanel'),
    path('home/',views.home,name='home'),
    path('createblog/',views.createblog,name='createblog'),
    path('takecourse/<int:courseid>',views.takeCourse,name='takecourse'),
    path('course-basket',views.courseBasket,name='course-basket'),
    path('deletecourse/<int:courseid>',views.unselectCourse,name='deletecourse'),
    path('subscribecourse/<int:courseid>',views.subscribeCourse,name='subscribecourse'),
    path('unsubscribecourse/<int:courseid>',views.unsubscribeCourse,name='unsubscribecourse'),
    path('postblog/',views.postblog,name='postblog'),
    path('readblog/<int:id>',views.readblog,name='readblog'),
    path('login/',views.login,name='login'),
    path('thanks/',views.thanks,name='thanks'),
    path('logout/',views.logout,name='logout'),
    path('messageus/<str:userid>',views.messageus,name='messageus'),
    path('completepurchase/',views.completepurchase,name='completepurchase'),
    path('profile',views.profile,name='profile'),
    path('removecartitem/<str:pk>',views.removecartitem,name='removecartitem'),
    path('productdetails/<int:itemid>',views.productdetails,name='productdetails'),
    path('shoppingcart/',views.shoppingcart,name='shoppingcart'),
    path('updatecart/',views.updatecart,name='updatecart'),
    path('checkout/',views.checkout,name='checkout'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('class/<str:pk>',views.Class,name='class'),
    path('buyItem/<str:pk>',views.buyItem,name='buyItem'),
    path('blogdetails/',views.blogdetails,name='blogdetails'),
    path('blog/',views.blog,name='blog'),
    path('contact/',views.contact,name='contact'),
    path('gallery/',views.gallery,name='gallery'),
    path('register/',views.register,name='register'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    path('addToWishlist/<str:id>',views.addToWishlist,name='addToWishlist'),
    path('removewishitem/<str:pk>',views.removewishitem,name='removewishitem'),
    path('createcomment/',views.createcomment,name='createcomment'),
    path('rate/<int:star_no>',views.rate,name='rate'),
    path('shop/',views.ShopView.as_view(),name='shop'),
    path('searchitem/',views.searchitem,name='searchitem'),
    path('updatesocials/<int:id>',views.updatesocials,name='updatesocials'),
    path('register_for_class/',views.classSignup,name='classSignup'),

    path("payment/waiting/<str:reference>/", views.paymentWaiting, name="payment_waiting"),

    path('api/payment/callback/', views.handle_payment_callback, name='handle_payment_callback'),
    path("check-payment-status/<str:reference>/", views.check_payment_status, name="check_payment_status"),

    # custom-admin activities
    
    path('additem/',views.additem,name='additem'),
    path('deleteitem/<int:id>',views.deleteitem,name='deleteitem'),
    path('modifyitem/<int:id>',views.modifyitem,name='modifyitem'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # path('shop/',views.shop,name='shop'),