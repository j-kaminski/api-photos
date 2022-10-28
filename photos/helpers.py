import requests

class PhotoExtractorData:
    @staticmethod
    def download_raw_photo(url):
        if not url.endswith(".png"):
            url = f"{url}.png"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return response.raw

    @staticmethod
    def extract_photo_size(url):
        photo_index = -2
        width = url.split("/")[photo_index]
        height = width
        return (width, height)

    @staticmethod
    def extract_photo_color(url):
        color_index = -1
        color = url.split("/")[color_index]
        return f"#{color}"