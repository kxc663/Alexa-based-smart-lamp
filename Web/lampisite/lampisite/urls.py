"""lampisite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings

extra_context = {}

urlpatterns = [
    path('lampi/', include('lampi.urls'), name='lampi'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(
         template_name='lampi/login.html',
         extra_context=extra_context), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
          template_name='lampi/logout.html',
         extra_context=extra_context), name='logout'),
    path('', RedirectView.as_view(pattern_name='lampi:index'), name='root'),
]
