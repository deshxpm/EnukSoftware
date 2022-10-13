from django.urls import path
from .views import *

urlpatterns = [

    path('', api, name="api"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('image-upload/', ImageUpload.as_view(), name="image-upload"),


]