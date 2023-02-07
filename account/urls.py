from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (
    login_view,
    register_view,
    verify_otp_view,
    complete_register_view,
    user_profile_view,
    UserFavoriteProductView,
    user_add_delete_favorite_product_view,
    UserAddressListView
)

app_name = 'account'
urlpatterns = [
    path('', user_profile_view, name='user-profile'),

    path('login/', login_view, name='otp-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='otp-register'),
    path('otp/verify', verify_otp_view, name='otp-verify'),
    path('register/complete', complete_register_view, name='complete-register'),

    path('favorites/', UserFavoriteProductView.as_view(), name='user-favorite-product'),
    path('favorites/add', user_add_delete_favorite_product_view, name='user-favorite-product-add-delete'),

    path('address/', UserAddressListView.as_view(), name='user-address-list'),
]
