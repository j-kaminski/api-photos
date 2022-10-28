from rest_framework import serializers
from ..models import Photo
import requests
import re


def validator_image_data_url(url):
    match = re.findall(r'/(\d+)/([a-fA-F0-9]+)(.\w+$|$)', url)[0]
    print(match)
    if match:
        return url 

    raise serializers.ValidationError("URL image doesn't include size or color")


class URLSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=200, validators=[validator_image_data_url])


class PhotoSerializer(serializers.ModelSerializer):
    albumId = serializers.IntegerField(source="album_id")

    class Meta:
        model = Photo
        fields = [
            "id",
            "title",
            "albumId",
            "url",
            "width",
            "height",
            "color"
        ]  # add image

        # def validate_url(self, value):
        #     print(value)
        def validate(self, data):
            print('here', data)
            return 

