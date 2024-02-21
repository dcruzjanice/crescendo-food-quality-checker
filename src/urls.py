from django.contrib import admin
from django.urls import path, include
from .views  import main_home
urlpatterns = [
    path('accounts/', include('accounts.urls')),  # Accounts URLs
    path('brand/', include('brand.urls')),        # Brand URLs
    path('admin/', admin.site.urls),
    path('', main_home, name='main_home'),
    path('api/', include('product.urls')),
    path('inspector/', include('inspector.urls')),  # Add this line

]
