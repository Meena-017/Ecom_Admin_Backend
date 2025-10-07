from django.urls import path
from website.api import views
from rest_framework.authtoken import views as drf_views
app_name = "api"
urlpatterns = [
    path('token/', drf_views.obtain_auth_token, name='api_token_auth'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('products/create/', views.product_list, name='product_create'),
    path('users/', views.user_list_api, name='user_list_api'),  # GET, POST
    path('users/<int:id>/', views.user_detail_api, name='user_detail_api'),  # GET, PUT, DELETE

]