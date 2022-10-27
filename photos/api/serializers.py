from rest_framework import serializers
from ..models import Photo
import requests
import re


# https://via.placeholder.com/600/88c71d"
def image_data(url):
    color_index = -1
    size_index = -2
    url_tokens = url.split("/")
    if len(url_tokens) > 2:
        color = url_tokens[color_index]
        size = url_tokens[size_index]
        # TODO match hex
        if size.isnumeric():
            return url

    raise serializers.ValidationError("URL image doesn't include size or color")


class URLSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=200, validators=[image_data])


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
