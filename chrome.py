import time
from selenium import webdriver

class Chrome(webdriver.Chrome):
    def __init__(self, site: str, width: int):
        print(f"Loading website: {site}, width: {width}", end="", flush=True)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-browser-side-navigation")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")

        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option(
            "prefs", {"download.prompt_for_download": False}
        )
        super(Chrome, self).__init__(options=chrome_options)
        try:
            self.set_window_size(width, 200)
            self.get(site)
            time.sleep(3)
            print(" [done]", flush=True)
        except Exception as e:
            self.close()
            self.quit()
            raise e

