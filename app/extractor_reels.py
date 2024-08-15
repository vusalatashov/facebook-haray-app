import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from app.login import login_to_facebook

reels_count = 0
def extract_urls(driver_reels, postgres):
    global reels_count
    try:
        elements = WebDriverWait(driver_reels, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@class="x6s0dn4 x18l40ae x5yr21d x1n2onr6 xh8yej3"]')
        ))
        for element in elements:
            video_id = element.get_attribute("data-video-id")
            if video_id and video_id:
                reels_count += 1
                if reels_count % 10 == 0:
                    print("Sleeping for 60 seconds...")
                    time.sleep(60)
                url = f"https://www.facebook.com/watch?v={video_id}"
                postgres.save_video(url, video_id)
                yield url
    except Exception as e:
        print(f"Error during reels url extraction")


def click_next(driver_reels):
    try:
        next_button = WebDriverWait(driver_reels, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Növbəti kart" and @role="button"]'))
        )
        driver_reels.execute_script("arguments[0].click();", next_button)
        time.sleep(2)
    except Exception as e:
        print(f"Error during clicking next")


def fetch_urls(driver_reels, postgres):
    login_to_facebook(driver_reels)
    driver_reels.get("https://www.facebook.com/reel")
    driver_reels.implicitly_wait(1)
    time.sleep(0.5)

    while True:
        try:
            for url in extract_urls(driver_reels, postgres):
                pass
            click_next(driver_reels)
        except Exception as e:
            print(f"Loop terminated due to error")
            break



