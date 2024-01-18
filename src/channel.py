import os
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


class Channel:
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str):
        """Класс для ютуб-канала"""
        self.channel_id = channel_id
        self.channel_data = self.get_channel_data()
        self.title = self.channel_data["items"][0]["snippet"]["title"]
        self.description = self.channel_data["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = self.channel_data["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel_data["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel_data["items"][0]["statistics"]["viewCount"]

    def get_channel_data(self):
        """Получает данные о канале
        из YouTube Data API."""
        youtube = self.get_service()
        request = youtube.channels().list(
            part="snippet,statistics",
            id=self.channel_id
        )
        response = request.execute()
        return response

    def to_json(self, file_name):
        """Сохраняет данные о канале в
        формате JSON в указанный файл."""
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=2)

    @classmethod
    def get_service(cls):
        """Создает и возвращает объект
         YouTube Data API сервиса."""
        return build('youtube', 'v3', developerKey=cls.api_key)
