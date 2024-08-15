import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.postgres_video import PostgresVideo
from app.extractor_video import fetch_urls as fetch_video_urls
from app.extractor_reels import fetch_urls as fetch_reels_urls
from app.dowlnoad_video import download_video
from app.driver import create_driver
from app.extractor_info import extract_info
from app.login import login_to_facebook


class Main:
    def __init__(self):
        # self.driver_video = create_driver()
        self.driver_reels = create_driver()
        self.driver_video_info = create_driver()
        self.driver_user_info = create_driver()
        self.postgres = PostgresVideo()

        self.urls_for_video = list()
        self.executor = ThreadPoolExecutor(max_workers=4)

    # async def extract_video_urls(self):
    #     print("Video URL extraction starting")
    #     loop = asyncio.get_running_loop()
    #     await loop.run_in_executor(self.executor, fetch_video_urls, self.driver_video, self.postgres)
    #     self.driver_video.quit()
    #
    # async def extract_reels_urls(self):
    #     print("Reels URL extraction starting")
    #     loop = asyncio.get_running_loop()
    #     await loop.run_in_executor(self.executor, fetch_reels_urls, self.driver_reels, self.postgres)
    #     self.driver_reels.quit()

    async def extract_video_info_and_user_url(self):
        print("Video info and extraction starting")
        while True:
            self.urls_for_video = self.postgres.find_urls()
            if not self.urls_for_video:
                print("No URLs found, waiting...")
                await asyncio.sleep(5)
                continue
            print(self.urls_for_video)
            for url_tuple in self.urls_for_video:
                if not url_tuple:
                    continue
                url = url_tuple[0]
                loop = asyncio.get_running_loop()
                self.driver_video_info.get("https://www.facebook.com")
                login_to_facebook(self.driver_video_info)
                self.driver_user_info.get("https://www.facebook.com")
                login_to_facebook(self.driver_user_info)
                await loop.run_in_executor(self.executor, extract_info, url, self.driver_video_info,
                                           self.driver_user_info, self.postgres)
                # await loop.run_in_executor(self.executor, download_video, url, self.postgres)
                await asyncio.sleep(1)
        self.driver_video_info.quit()
        self.driver_user_info.quit()
    async def run(self):
        # task1 = asyncio.create_task(self.extract_video_urls())
        # task2 = asyncio.create_task(self.extract_reels_urls())
        task3 = asyncio.create_task(self.extract_video_info_and_user_url())

        await asyncio.gather( task3)


if __name__ == "__main__":
    main = Main()
    asyncio.run(main.run())
