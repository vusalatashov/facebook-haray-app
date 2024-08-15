import sys
from facebook_downloader.downloader import FacebookDownloader

def download_video(video_url, postgres):
    sys.argv = ['script_name', video_url, '--audio', '-o', '/Users/macbook/Desktop/Development/Haray_Facebook/resources/video_resources/']
    downloader = FacebookDownloader()

    try:
        downloader.download_video()
    except Exception as e:
        print(f"Error occurred: {e}")

