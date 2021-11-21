from django.contrib import admin
from django.urls import path
from nasa_api.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home)
]