import re

from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from app.driver import create_driver
from app.login import login_to_facebook
from app.postgres_video import PostgresVideo


def parse_count(count_str):
    count_str = count_str.lower().replace(' rəy', '').replace(' comments', '').replace(' comments', '').replace(' ',
                                                                                                                '').strip()
    match = re.match(r'([\d\.]+)([kmb]?)', count_str)
    if not match:
        return 0
    number, suffix = match.groups()
    number = float(number)
    if suffix == 'k':
        return int(number * 1_000)
    elif suffix == 'm':
        return int(number * 1_000_000)
    elif suffix == 'b':
        return int(number * 1_000_000_000)
    else:
        return int(number)


def extract_info_reels(url, driver_video_info1, driver_user_info1, postgres1):
    try:
        soup = soup_info(driver_video_info1, url)
        like_count = get_like_count_reels(soup)
        comment_count = get_comment_count_reels(soup)
        user_name = get_user_name_reels(soup)
        user_url = get_user_url_reels(soup)
        description = get_description_reels(soup)

        if user_url != 'N/A' and 'watch' not in user_url :
            postgres1.save_video_info(like_count, comment_count, description, url)
            if 'instagram' not in user_url:
                follower, following = extract_user_info(driver_user_info1, user_url)
                postgres1.save_user_url(user_url, user_name, follower, following, url)
        else:
            postgres1.delete_video(url)
        return {
            "Username": user_name,
            "Likes": like_count,
            "Comments": comment_count,
            "Description": description,
        }
    except Exception as e:
        print(f"Error extracting reels info")
        return None


def extract_info_video(url, driver_video_info1, driver_user_info1, postgres1):
    try:
        soup = soup_info(driver_video_info1, url)
        like_count = get_like_count_video(soup)
        comment_count = get_comment_count_video(soup)
        user_name = get_user_name_video(soup)
        user_url = get_user_url_video(soup)
        description = get_description_video(soup)

        if user_url == "N/A" and user_name == "N/A" and like_count == 0:
            return extract_info_reels(url, driver_video_info1, driver_user_info1, postgres1)
        else:
            follower, following = extract_user_info(driver_user_info1, user_url)

            postgres1.save_video_info(like_count, comment_count, description, url)
            postgres1.save_user_url(user_url, user_name, follower, following, url)
            return {
                "Username": user_name,
                "Likes": like_count,
                "Comments": comment_count,
                "Description": description,
            }

    except Exception as e:
        print(f"Error extracting video info")
        return None


def extract_info(url, driver_video_info, driver_user_info, postgres):
    video_info = extract_info_video(url, driver_video_info, driver_user_info, postgres)
    if video_info is None or (video_info['Username'] == 'N/A' and video_info['Views'] == 0):
        return extract_info_reels(url, driver_video_info, driver_user_info, postgres)
    return video_info


def get_like_count_video(soup):
    like_count_elements = soup.find_all('span', class_='x6ikm8r x10wlt62 xlyipyv')
    like_count = 0
    if like_count_elements:
        like_count_text = like_count_elements[0].find('span',
                                                      class_='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j').text
        if like_count_text:
            return extract_integer(like_count_text)
            # like_count = parse_count(like_count_text) if like_count_text != 'N/A' else 0
    return like_count


def get_view_count_video(soup):
    view_count_elements = soup.find_all('span',
                                        class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa')
    view_count = 0
    if view_count_elements and len(view_count_elements) > 1 and 'views' in view_count_elements[1].text.lower():
        view_count = parse_count(view_count_elements[1].text.lower())
    return view_count


def get_comment_count_video(soup):
    comment_count_elements = soup.find_all('span',
                                           class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa')
    comment_count = 0
    if comment_count_elements and len(comment_count_elements) > 0 and ('rəy' or 'comments') in comment_count_elements[0].text.lower():
        comment_count = parse_count(comment_count_elements[0].text.lower())
    return comment_count


def get_description_video(soup):
    description_element = soup.select_one(
        'div.x1jx94hy.x6ikm8r.x10wlt62.x1ye3gou.xn6708d.xyamay9.x1l90r2v span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6')
    description = description_element.text.strip() if description_element else 'N/A'
    return description


def get_user_url_video(soup):
    user_url_element = soup.find_all('a',
                                     class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u')
    user_url = 'N/A'
    if user_url_element:
        user_url = user_url_element[0].get('href') if user_url_element else 'N/A'
        user_url = user_url.split('?')[0] if user_url != 'N/A' else 'N/A'
    return user_url


def get_user_name_video(soup):
    user_name_element = soup.select_one('div.x78zum5.xdt5ytf.xz62fqu.x16ldp7u h2.html-h2 a.x1i10hfl')
    user_name = user_name_element.text.strip() if user_name_element else 'N/A'
    return user_name


def get_like_count_reels(soup):
    like_count_element = soup.find_all('span', {'class': 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft'})
    like_count = like_count_element[3].get_text() if len(like_count_element) > 3 else 'N/A'
    like_count = re.sub(r'\D', '', like_count) if like_count != 'N/A' else ''
    like_count = int(like_count) if like_count else 0
    return like_count


def get_comment_count_reels(soup):
    comment_count_element = soup.find_all('span', {'class': 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft'})
    comment_count = comment_count_element[4].get_text() if len(comment_count_element) > 4 else 'N/A'
    comment_count = re.sub(r'\D', '', comment_count) if comment_count != 'N/A' else ''
    comment_count = int(comment_count) if comment_count else 0
    return comment_count


def get_user_url_reels(soup):
    user_url_element = soup.find_all('a',
                                     class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3')
    user_url = user_url_element[0].get('href') if user_url_element else 'N/A'
    if 'instagram' in user_url:
        return user_url
    user_url = "https://www.facebook.com" + user_url.split('&')[0] if user_url != 'N/A' else 'N/A'
    return user_url


def get_user_name_reels(soup):
    user_name_element = soup.find_all('a', {
        'class': 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3'})
    user_name = user_name_element[1].get_text() if len(user_name_element) > 0 else 'N/A'
    return user_name


def get_description_reels(soup):
    description_element = soup.find_all('div', {'class': 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a'})
    description = description_element[0].get_text() if description_element else 'N/A'
    return description


def soup_info(driver_video_info1, url):
    driver_video_info1.get(url)
    WebDriverWait(driver_video_info1, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver_video_info1.page_source, 'html.parser')
    return soup


def extract_user_info(driver_user_info1, user_url):
    follower_count = 0
    following_count = 0
    soup = soup_info(driver_user_info1, user_url)
    user_info = soup.find_all('a',
                              class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xi81zsa x1s688f')
    if len(user_info) < 2:
        return follower_count, following_count

    follower_count_str = user_info[0].get_text()
    following_count_str = user_info[1].get_text()

    follower_count=parse_count(follower_count_str)
    following_count=parse_count(following_count_str)
    return follower_count, following_count

def extract_integer(s):
    # Remove non-numeric characters except for periods and abbreviations
    cleaned = ''.join(c if c.isdigit() or c == '.' or c in 'KkM' else '' for c in s)

    # Replace K and M with their numeric multipliers
    if 'K' in cleaned or 'k' in cleaned:
        cleaned = cleaned.replace('K', '').replace('k', '')
        number = int(float(cleaned) * 1000)
    elif 'M' in cleaned:
        cleaned = cleaned.replace('M', '')
        number = int(float(cleaned) * 1000000)
    else:
        # Remove periods and convert to integer
        number = int(cleaned.replace('.', ''))

    return number



if __name__ == "__main__":
    postgres2 = PostgresVideo()
    driver_video_info2 = create_driver()
    driver_user_info2 = create_driver()
    driver_video_info2.get("https://www.facebook.com")
    login_to_facebook(driver_video_info2)
    driver_user_info2.get("https://www.facebook.com")
    login_to_facebook(driver_user_info2)

    extract_info("https://www.facebook.com/reel/1217413092753221", driver_video_info2, driver_user_info2, postgres2)
    driver_user_info2.quit()
    driver_video_info2.quit()
