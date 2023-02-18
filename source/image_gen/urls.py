from django.urls import path
from .views import CreateImageView

urlpatterns = [
    path('create_image', CreateImageView.as_view(), name="create_image"),
   
]
