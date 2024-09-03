import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from driver.login import login_to_facebook

def extract_urls(driver_video, postgres, processed_urls):
    try:
        elements = WebDriverWait(driver_video, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH,
             '//*[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 xo1l8bm"]')
        ))
        for i, element in enumerate(elements, 1):
            video_link = "https://www.facebook.com" + \
                         BeautifulSoup(element.get_attribute("outerHTML"), 'html.parser').a['href'].split('&')[0]
            if video_link not in processed_urls:
                postgres.save_video(video_link, video_link.split('?v=')[1])
                processed_urls.add(video_link)
            if len(processed_urls) >= 10:
                return
    except Exception as e:
        print(f"Error during video URL extraction: {e}")

def fetch_urls_video(driver_video, postgres):
    # login_to_facebook(driver_video)
    driver_video.get("https://www.facebook.com/watch")
    time.sleep(6)

    processed_urls = set()

    while len(processed_urls) < 10:
        extract_urls(driver_video, postgres, processed_urls)
        driver_video.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
