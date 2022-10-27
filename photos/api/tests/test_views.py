import os
import json
import requests
import shutil
from pathlib import Path
from unittest import mock
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings
from django.urls import reverse
from django.core.files.images import ImageFile
from photos.models import Photo
from photos.api.serializers import PhotoSerializer


MOCK_IMG_PATH = "photos/api/tests/mock-img-600-92c952.png"
TEST_PHOTOS_PATH = Path("assets", settings.PHOTOS_DIR)


class MockResponse:
    def __init__(self):
        self.raw = ImageFile(open(MOCK_IMG_PATH, "rb"), "mock-img-600-92c952")
        self.status_code = 200


def make_image_mock(data, stream):
    return MockResponse()

class TestPhotoList(APITestCase):
    def setUp(self):
        TEST_PHOTOS_PATH.mkdir(exist_ok=True)

    def tearDown(self):
        shutil.rmtree(TEST_PHOTOS_PATH)
    
    def create_photo(self):
        photo_data = {
            "title": "p1_photo",
            "album_id": 1,
            "url": "https://mock-photos.com/600/92c952",
            "width": 600,
            "height": 600,
            "color": "#92c952",
        }
        return Photo.objects.create(**photo_data)


class TestPhotoDetail(APITestCase):
    def setUp(self):
        TEST_PHOTOS_PATH.mkdir(exist_ok=True)

    def tearDown(self):
        shutil.rmtree(TEST_PHOTOS_PATH)
    
    def create_photo(self):
        photo_data = {
            "title": "p1_photo",
            "album_id": 1,
            "url": "https://mock-photos.com/600/92c952",
            "width": 600,
            "height": 600,
            "color": "#92c952",
        }
        return Photo.objects.create(**photo_data)

    @mock.patch("requests.get", mock.Mock(side_effect=make_image_mock))
    def test_post_photo(self):
        photo_json = {
            "title": "p1_photo",
            "albumId": 1,
            "url": "https://mock-photos.com/600/92c952",
        }
        response = self.client.post(reverse("photo_list_create"), photo_json)
        self.assertEqual(response.status_code, 200)
        photos = Photo.objects.all()
        self.assertEqual(photos.count(), 1)
        created_photo = Photo.objects.all().first()

        expected_response = {
            "id": 1,
            "title": "p1_photo",
            "albumId": 1,
            "url": "https://mock-photos.com/600/92c952",
            "width": 600,
            "height": 600,
            "color": "#92c952",
        }
        self.assertEqual(expected_response, response.data)
        self.assertEqual(created_photo.image.name, os.path.join(settings.PHOTOS_DIR, '600_92c952.png'))
        self.assertTrue(os.path.isfile(os.path.join("assets", created_photo.image.name)))

    def test_post_photo_same_url(self):
        p = self.create_photo()
        self.assertEqual(Photo.objects.all().count(), 1)
        photo_json = {
            "title": p.title,
            "albumId": p.album_id,
            "url": p.url,
        }
        response = self.client.post(reverse("photo_list_create"), photo_json)
        self.assertEqual(response.data, 'photo exists')
        self.assertEqual(Photo.objects.all().count(), 1)

    def test_post_photo_invalid_url(self):
        # photo_json = {"title": "p1_photo", "album_id": 1, "url": "https://mock-photos/600/92c952"}
        # response = client.post(reverse("post_photos"), photo_json)
        # expected_response = {}
        # self.assertEqual(expected_response, response.data)
        pass

    def test_post_photo_missing_data(self):
        pass
        # photo_json = {"title": "p1_photo", "album_id": 1, "url": "https://mock-photos.com/600/92c952"}
        # response = client.post(reverse("post_photos"), photo_json)

    def test_post_photo_invalid_data(self):
        pass
        # photo_json = {"title": "p1_photo", "album_id": 1, "url": "https://mock-photos.com/600/92c952"}
        # response = client.post(reverse("post_photos"), photo_json)

    def test_post_photo_url_without_png_extension(self):
        pass
    
    def test_get_photo(self):
        p = self.create_photo()


