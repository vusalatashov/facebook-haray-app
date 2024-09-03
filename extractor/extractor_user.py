# from selenium.webdriver.support import expected_conditions as EC
#
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from bs4 import BeautifulSoup
#
#
#
# def extract_user_urls_for_video(driver,driver_user_info, url, postgres):
#     driver.get(url)
#     try:
#         elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(
#             (By.XPATH,
#              '//*[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u"]')
#         ))
#         for element in elements:
#             user_url = element.get_attribute("href")
#             postgres.save_user_url(user_url, follower_count, following_count)
#             return user_url
#
#     except Exception as e:
#         print(f"Error during extraction: {e}")
#         return []
#
#
# def extract_user_urls_for_reels(driver,driver_user_info, url, postgres):
#     driver.get(url)
#     try:
#         elements = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located(
#             (By.XPATH,
#              '//*[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3"]')
#         ))
#         for element in elements:
#             full_url = element.get_attribute("href")
#             if full_url:
#                 user_url_part = full_url.split('&')[0]
#                 follower_count,following_count=extract_user_info(driver_user_info,user_url_part)
#                 postgres.save_user_url(user_url_part)
#                 return user_url_part
#     except Exception as e:
#         print(f"Error during extraction: {e}")
#         return []
#
#
# def extract_user(driver,driver_user_info, url, postgres):
#     user_url = extract_user_urls_for_video(driver,driver_user_info, url, postgres)
#     if "people" not in user_url:
#         return extract_user_urls_for_reels(driver,driver_user_info, url, postgres)
#     return user_url
#
#
