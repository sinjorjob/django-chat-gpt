from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('proofreading.urls')), 
    path('', include('image_gen.urls')),  #追加
]
