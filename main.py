import os
import asyncio

from config.config import ROOT_DIR
from driver.driver import Driver
from driver.login import login_to_facebook
from extractor.extractor_info import extract_info
from database.postgres_video import PostgresVideo
from download.dowlnoad_video import download_videos
from extractor.extractor_reels import fetch_reels_urls
from convert.speech_to_text import speech_to_text
from download.speech_detection import main_detect

os.chdir(ROOT_DIR)


async def run():
    driver = Driver()
    while True:
        driver_reels = driver.create_driver()
        driver_video_info = driver.create_driver()
        driver_user_info = driver.create_driver()
        postgres = PostgresVideo()
        login_to_facebook(driver_reels)
        for i in range(0, 10):
            await fetch_reels_urls(driver_reels, postgres)
            await extract_info(driver_video_info, driver_user_info, postgres)
            await download_videos(postgres)
            await main_detect(postgres)
            await speech_to_text(postgres)
        driver_reels.quit()
        driver_video_info.quit()
        driver_user_info.quit()



if __name__ == "__main__":
    asyncio.run(run())
