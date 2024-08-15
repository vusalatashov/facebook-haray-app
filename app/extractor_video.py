import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from app.login import login_to_facebook


video_count = 0


def extract_urls(driver_video, postgres):
    global video_count
    try:
        elements = WebDriverWait(driver_video, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH,
             '//*[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 xo1l8bm"]')
        ))
        for element in elements:
            element_html = element.get_attribute("outerHTML")
            soup = BeautifulSoup(element_html, 'html.parser')
            whole_link = soup.a['href']
            video_id = whole_link.split('?v=')[1]
            video_id = video_id.split('&')[0]
            if '/watch/?v=' in whole_link:
                video_link = "https://www.facebook.com" + whole_link.split('&')[0]
                video_count += 1
                if video_count % 10 == 0:
                    print("Sleeping for 60 seconds...")
                    time.sleep(60)
                postgres.save_video(video_link, video_id)
    except Exception as e:
        print(f"Error during video url extraction")


def scroll_down(driver_video):
    driver_video.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


def fetch_urls(driver_video, postgres):
    login_to_facebook(driver_video)
    driver_video.get("https://www.facebook.com/watch")
    driver_video.implicitly_wait(1)
    time.sleep(5)

    while True:
        extract_urls(driver_video, postgres)
        scroll_down(driver_video)
