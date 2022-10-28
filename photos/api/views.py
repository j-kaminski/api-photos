from django.core.files.uploadedfile import UploadedFile
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from .serializers import PhotoSerializer, URLSerializer
from ..models import Photo
from ..helpers import PhotoExtractorData

class PhotoList(ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def post(self, request, **kwargs):
        url = request.data["url"]
        url_serializer = URLSerializer(data={"url": url})
        if url_serializer.is_valid():
            if not Photo.objects.filter(url=url).exists():
                height, width = PhotoExtractorData.extract_photo_size(url)
                color = PhotoExtractorData.extract_photo_color(url)
                image = UploadedFile(
                    PhotoExtractorData.download_raw_photo(url), f"{height}_{color}.png"
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
                        content=PhotoExtractorData.download_raw_photo(url),
                    )  # TODO: should be called in save
                    return Response({**photo_serializer.data, 'id': p.pk})

                return Response(photo_serializer.errors)
            else:
                return Response('photo exists') # TODO: should return better error
        return Response(url_serializer.errors)


class PhotoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def patch(self, request, **kwargs):
        print(request)
        return Response()
