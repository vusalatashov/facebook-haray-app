import os
import asyncio

from config.config import ROOT_DIR
from driver.driver import create_driver
from driver.login import login_to_facebook
from extractor.extractor_info import extract_info
from database.postgres_video import PostgresVideo
from download.dowlnoad_video import download_videos
from extractor.extractor_video import fetch_urls_video
from extractor.extractor_reels import fetch_reels_urls
from convert.speech_to_text import speech_to_text

os.chdir(ROOT_DIR)


class Main:
    def __init__(self):
        self.driver_video = create_driver()
        self.driver_reels = create_driver()
        self.driver_video_info = create_driver()
        self.driver_user_info = create_driver()
        self.postgres = PostgresVideo()

    def login_to_driver(self):
        login_to_facebook(self.driver_video)
        login_to_facebook(self.driver_reels)

    async def extract_video_urls(self):
        fetch_urls_video(self.driver_video, self.postgres)

    async def extract_reels_urls(self):
        fetch_reels_urls(self.driver_reels, self.postgres)

    async def extract_video_info_and_user_url(self):
        urls = self.postgres.find_urls()
        extract_info(urls, self.driver_video_info, self.driver_user_info, self.postgres)

    async def download_videos(self):
        urls = self.postgres.get_post_url_for_download()
        await download_videos(urls, self.postgres)

    async def speech_to_text(self):
        mp3_paths = self.postgres.get_url_for_content()
        await speech_to_text(self.postgres, mp3_paths)

    def run(self):
        self.login_to_driver()
        while True:
            # asyncio.run(self.extract_video_urls())
            asyncio.run(self.extract_reels_urls())
            asyncio.run(self.extract_video_info_and_user_url())
            asyncio.run(self.download_videos())
            asyncio.run(self.speech_to_text())


if __name__ == "__main__":
    Main().run()
