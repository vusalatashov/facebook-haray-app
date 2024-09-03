import logging
import os
from platform import system
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

logging.getLogger('undetected_chromedriver').setLevel(logging.CRITICAL)
logging.getLogger('webdriver_manager').setLevel(logging.CRITICAL)


class Driver:
    def get_options(self):
        options = uc.ChromeOptions()
        options.headless = False
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--mute-audio")
        options.add_argument("--lang=az-AZ")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--headless=new')
        options.add_argument("--disable-blink-features=AutomationControlled")

        return options

    def install_driver(self) -> str:
        path = ChromeDriverManager(driver_version="127.0.6533.120").install()
        platform = system()

        if platform == "Windows":
            path = path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
        else:
            path = path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver")
        os.chmod(path, 0o755)
        return path

    def create_driver(self) -> uc.Chrome:
        options = self.get_options()
        path = self.install_driver()
        self.driver = uc.Chrome(executable_path=path, options=options, use_subprocess=False, headless=False)
        self.driver.maximize_window()

        return self.driver
