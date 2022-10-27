import requests
from django.core.files.uploadedfile import UploadedFile
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .serializers import PhotoSerializer, URLSerializer
from ..models import Photo


class PhotoList(ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def _download_raw_photo(self, url):
        if not url.endswith(".png"):
            url = f"{url}.png"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return response.raw

    def _extract_photo_size(self, url):
        photo_index = -2
        width = url.split("/")[photo_index]
        height = width
        return (width, height)

    def _extract_photo_color(self, url):
        color_index = -1
        color = url.split("/")[color_index]
        return f"#{color}"

    def post(self, request, **kwargs):
        print(request.data)
        return Response()
        url_serializer = URLSerializer(data={"url": request.data["url"]})
        if url_serializer.is_valid():
            url = url_serializer.data["url"]
            if not Photo.objects.filter(url=url).exists():
                height, width = self._extract_photo_size(url)
                color = self._extract_photo_color(url)
                image = UploadedFile(
                    self._download_raw_photo(url), f"{height}_{color}.png"
                )
                photo_data = {
                    **request.data,
                    "height": height,
                    "width": width,
                    "color": color,
                    "image": image,
                }
                for key, val in request.data.items():
                    photo_data[key] = val

                photo_serializer = PhotoSerializer(data=photo_data)
                if photo_serializer.is_valid():
                    p = photo_serializer.save()
                    p.image.save(
                        name=f"{height}_{color}.png",
                        content=self._download_raw_photo(url),
                    )  # TODO: should be called in save
                    return Response({**photo_serializer.data, 'id': p.pk})

                return Response(photo_serializer.errors)
            else:
                return Response('photo exists') # TODO: should return better error


class PhotoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def _download_raw_photo(self, url):
        if not url.endswith(".png"):
            url = f"{url}.png"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return response.raw

    def _extract_photo_size(self, url):
        photo_index = -2
        width = url.split("/")[photo_index]
        height = width
        return (width, height)

    def _extract_photo_color(self, url):
        color_index = -1
        color = url.split("/")[color_index]
        return f"#{color}"

    # def post(self, request, **kwargs):
    #     url_serializer = URLSerializer(data={"url": request.data["url"]})
    #     if url_serializer.is_valid():
    #         url = url_serializer.data["url"]
    #         if not Photo.objects.filter(url=url).exists():
    #             height, width = self._extract_photo_size(url)
    #             color = self._extract_photo_color(url)
    #             image = UploadedFile(
    #                 self._download_raw_photo(url), f"{height}_{color}.png"
    #             )
    #             photo_data = {
    #                 **request.data,
    #                 "height": height,
    #                 "width": width,
    #                 "color": color,
    #                 "image": image,
    #             }
    #             for key, val in request.data.items():
    #                 photo_data[key] = val

    #             photo_serializer = PhotoSerializer(data=photo_data)
    #             if photo_serializer.is_valid():
    #                 p = photo_serializer.save()
    #                 p.image.save(
    #                     name=f"{height}_{color}.png",
    #                     content=self._download_raw_photo(url),
    #                 )  # TODO: should be called in save
    #                 return Response({**photo_serializer.data, 'id': p.pk})

    #             return Response(photo_serializer.errors)
    #         else:
    #             return Response('photo exists') # TODO: should return better error

        return Response(url_serializer.errors)
    
    def patch(self, request, **kwargs):
        print(request)
        return Response()
