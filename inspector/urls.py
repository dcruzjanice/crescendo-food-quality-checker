# inspector/urls.py
from django.urls import path
from .views import inspection_list, products_of_brand, product_review,inspection_home

urlpatterns = [
    path('', inspection_list, name='inspection-list'),
    path('home/', inspection_home, name='inspection_home'),
    path('<str:username>/', products_of_brand, name='products_of_brand'),
    path('<str:username>/<int:product_id>/', product_review, name='product-review'),
]
