from django.urls import include, path
from rest_framework import routers
from .api.views import PhotoList, PhotoDetail 


urlpatterns = [path("photos/", view=PhotoList.as_view(), name="photo_list_create"),
               path("photos/<int:pk>/", view=PhotoDetail.as_view(), name="photo_detail")]

