"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from home.views import my_custom_page_not_found_view, my_custom_error_view

urlpatterns = [
    path("admin_prv/", admin.site.urls),
    path("", include("home.urls")),
    path("loan/", include("loan.urls")),
    path("forum/", include("forum.urls")),
    path("api_prv/forum/", include("forum.api.urls")),
    path("accounts/", include("accounts.urls")),
    path('accounts/', include('django.contrib.auth.urls')),

]


# 404 http views...
handler404 = my_custom_page_not_found_view
handler500 = my_custom_error_view