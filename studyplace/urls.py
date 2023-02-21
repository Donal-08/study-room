"""studyplace URL Configuration

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

# This is our CORE URLS FILE, we can have multiple urls files here but we are gonna use two here - root and one for a specific app

from django.contrib import admin
from django.urls import path, include
# from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home),                     # tell which fn we are gonna trigger when we open our home page('')
    # path('room/', room),                               # http://127.0.0.1:8000/room/

    path('', include('base.urls')),            # send the user to  base/urls.py (LET THE URLS FILE TAKE CARE OF ALL THE ROUTINGS i.r matching routes)   

]
