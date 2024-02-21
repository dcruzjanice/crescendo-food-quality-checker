from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', brand_home, name="brand_home"),
    path('register/', brand_register_attempt, name="brand_register_attempt"),
    path('login/', brand_login_attempt, name="brand_login_attempt"),
    path('token/', brand_token_send, name="brand_token_send"),
    path('success/', brand_success, name='brand_success'),
    path('verify/<auth_token>/', brand_verify, name="brand_verify"),
    path('error/', brand_error_page, name="brand_error"),
    path('logout/', brand_logout_view, name='brand_logout'),
    path('reset_password/', brand_password_reset, name='brand_password_reset'),
    path('reset_password/<str:auth_token>/', brand_password_reset_confirm, name='brand_password_reset_confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
