"""django_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from second_day import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path("names/",views.show_names),
    path("names/<int:cid>",views.show_favor),
    path("login/",views.login),
    path("login_submit/",views.login_submit),
    path("login_ajax/",views.login_ajax),
    path("login_ajax_handle/",views.login_ajax_handle),
    path("sset_cookie/",views.cookie_set),
    path("get_cookie/",views.cookie_get),
    path("set_session/",views.session_set),
    path("get_session/",views.session_get),
    path("filter_name/",views.filter_name),
    path("v1/",views.v1,name = "v1"),
    path("v2/",views.v2,name = "v2"),
]

