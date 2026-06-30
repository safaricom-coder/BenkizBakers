from django.urls import path
from . import views,adminViews

urlpatterns = [
    # ── Legacy endpoints ──
    path('', views.getAllItems),
    path('get/<int:id>', views.getItem),
    path('getcartitem/<int:id>', views.getCartItem),
    path('createitem/', views.createItem),
    path('deleteallitems/', views.delete_all_items),
    path('deleteuser/<int:id>', views.delete_user),
    path("handle_payment_callback/", views.handle_payment_callback),

    # ── Auth ──
    path('auth/csrf/', views.csrf_token_view),
    path('auth/login/', views.login_view),
    path('auth/logout/', views.logout_view),
    path('auth/register/', views.register_view),
    path('auth/me/', views.me_view),
    path('auth/refresh/', views.refresh),

    # ── Items ──
    path('items/', views.items_list),
    # path('items/?category=<str:category>',views.filter_by_category),
    path('items/featured/', views.items_featured),
    path('items/<int:id>/', views.item_detail),
    path('categories/', views.categories_list),

    # ── Cart ──
    path('cart/', views.cart_view),
    path('cart/add/', views.cart_add),
    path('cart/items/<int:id>/', views.cart_item_view),

    # ── Wishlist ──
    path('wishlist/', views.wishlist_view),
    path('wishlist/add/', views.wishlist_add),
    path('wishlist/remove/<int:item_id>/', views.wishlist_remove),

    # ── Classes ──
    path('lessons/', views.lessons_list),
    path('lessons/<int:id>/enroll/', views.lesson_enroll),
    path('lessons/<int:id>/unenroll/', views.lesson_unenroll),
    path('course-basket/', views.course_basket),

    # path('testenv/', views.test_env),

    # ── Profile ──
    path('profile/', views.profile_view),

    # ── Testimonials ──
    path('testimonials/', views.testimonials_list),

    # ── Team ──
    path('team/', views.team_list),

    # ── Locations ──
    path('locations/', views.locations_list),

    # ── Contact ──
    path('contact/', views.contact_send),

    # ── Checkout & Payments ──
    path('checkout/', views.checkout_view),
    path('payment-status/<str:reference>/', views.payment_status),

    # ── Hero Banners ──
    path('hero-banners/', views.hero_banners),

    # ── Stats ──
    path('stats/', views.stats_view),
    # ── TEAM ──
    path('stats/', views.team),
    # ── TESTIMONIALS ──
    path('stats/', views.testimonials),


    path('admin/products/',adminViews.getAdminProducts),

    path('admin/products/edit/',adminViews.editAdminProduct),
    path('admin/products/create/',adminViews.createAdminProduct),
]
