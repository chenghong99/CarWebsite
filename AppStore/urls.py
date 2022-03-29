"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.login, name='login'),
    path('index', app.views.index, name='index'),
    path('signup', app.views.signup, name='signup'),
    path('admin', app.views.admin, name='admin'),
    path('logout/', app.views.logout_page, name = "logout"),
    path('login', app.views.login, name='login'),
    path('addcar', app.views.addcar, name='addcar'),
    path('editpersonalinfo', app.views.editpersonalinfo, name='editpersonalinfo'),
    path('editpersonalinfoPH/<str:email>', app.views.editpersonalinfoPH, name='editpersonalinfoPH'),
    path('editpersonalcarinfo/<str:car_vin>', app.views.editpersonalcarinfo, name='editpersonalcarinfo'),
    path('editrentalcarinfo', app.views.editrentalcarinfo, name='editrentalcarinfo'),
    path('profile', app.views.profile, name='profile'),
    path('addpersonalinfo', app.views.addpersonalinfo, name='addpersonalinfo'), 
    path('personalcarinfoPH', app.views.personalcarinfoPH, name='personalcarinfoPH'),
    path('personalcarinfoPH/edit/<str:owner>/<str:car_vin>', app.views.editpersonalcarinfoPH, name='editpersonalcarinfoPH'),  
    path('addpersonalcarinfoPH', app.views.addpersonalcarinfoPH, name='addpersonalcarinfoPH'),   ######### edit info then need coz diff row diff displayed info in fields
    path('unavailablecarinfoPH', app.views.unavailablecarinfoPH, name='unavailablecarinfoPH'),
    path('unavailablecarinfoPH/edit/<str:car_vin>/<str:unavailable>', app.views.editunavailablecarinfoPH, name='editunavailablecarinfoPH'), ### goes to html file editunavailablecarinfo.html 
    path('addunavailablecarinfoPH', app.views.addunavailablecarinfoPH, name='addunavailablecarinfoPH'),
    path('rentalcarinfoPH', app.views.rentalcarinfoPH, name='rentalcarinfoPH'),
    path('rentalcarinfoPH/edit/<str:car_vin>/<str:pick_up>', app.views.editrentalcarinfoPH, name='editrentalcarinfoPH'),
    path('addrentalcarinfoPH', app.views.addrentalcarinfoPH, name='addrentalcarinfoPH'),

]


