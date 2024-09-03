import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def extract_urls(driver_reels, postgres, processed_urls):
    try:
        elements = WebDriverWait(driver_reels, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@class="x6s0dn4 x18l40ae x5yr21d x1n2onr6 xh8yej3"]')
        ))
        for element in elements:
            video_id = element.get_attribute("data-video-id")
            if video_id and video_id not in processed_urls:
                url = f"https://www.facebook.com/watch?v={video_id}"
                postgres.save_video(url, video_id)
                processed_urls.add(url)
                if len(processed_urls) >= 1:
                    return
    except Exception as e:
        print(f"Error during reels URL extraction: {e}")


def click_next(driver_reels):
    try:
        next_button = WebDriverWait(driver_reels, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Növbəti kart" and @role="button"]'))
        )
        driver_reels.execute_script("arguments[0].click();", next_button)
        time.sleep(2)
    except Exception as e:
        print(f"Error during clicking next: {e}")


def fetch_reels_urls(driver_reels, postgres):
    driver_reels.get("https://www.facebook.com/reel")
    time.sleep(0.5)

    processed_urls = set()

    while len(processed_urls) < 1:
        extract_urls(driver_reels, postgres, processed_urls)
        if len(processed_urls) < 1:
            click_next(driver_reels)

    return processed_urls
