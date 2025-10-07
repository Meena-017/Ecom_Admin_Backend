from django.urls import path, include
from . import views

urlpatterns = [
    # Auth
    path("", views.login_page, name="login"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("signup/", views.signup_page, name="signup"),

    # Dashboard
    path("dashboard/", views.dashboard_page, name="dashboard"),

    # FRONTEND Pages (unique names)
    path("product-list/", views.product_list_page, name="frontend_product_list"),
    path("user-list/", views.user_list_page, name="frontend_user_list"),

    # Cart
    path("cart/", views.cart_page, name="cart"),
    # path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    # path("remove-from-cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    # path('products/', views.product_list_page, name='frontend_product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # API
    path("api/", include("website.api.urls")),
]
