"""djangoProject3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from apps.authentication.views import Auth1View, Auth2View, DashboardView, WebhookView
from apps.banner.views import BannerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth1/', Auth1View.as_view()),
    path('auth2/', Auth2View.as_view()),
    path('dashboard/', DashboardView.as_view()),
    path('webhooks/', WebhookView.as_view()),
    path('banners/', BannerView.as_view()),
]
