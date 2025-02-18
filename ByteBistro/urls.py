"""
URL configuration for ByteBistro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path('api/', include('api.urls')),  # API base route (our APP)
    path('api/', include('djoser.urls')),  # Djoser route
    path('api/', include('djoser.urls.authtoken')),  # Djoser auth token route
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login route
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh JWT token route
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  # logout route
]
