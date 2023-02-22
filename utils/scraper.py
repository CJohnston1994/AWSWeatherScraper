from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, re, os, pprint, requests



class Met_Scraper():
    def __init__(self, browser = 'chrome'):
        self.url = "https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data"
        self.browser = browser
        self.pattern = 'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata'

    def set_browser_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        return options
    
    def open_browser(self):
        options = self.set_browser_options()
        self.driver = Chrome(service=Service(ChromeDriverManager().install()), options = options)
        self.driver.get(self.url)
        time.sleep(3)

    def gather_hrefs_by_pattern(self, url_pattern):
        links = self.driver.find_elements(By.CSS_SELECTOR, 'a')
        pattern = re.compile(url_pattern)
        matching_links = []
        for link in links:
            href = link.get_attribute('href')
            if href and pattern.match(href):
                matching_links.append(href)
        return matching_links
    
    def save_raw_data_locally(self, url_list : list) -> None:
        directory_path = os.path.join(os.getcwd(), "data", "raw")
        print(f"dirpath {directory_path}")

        print(directory_path)
        for url in url_list:
            response = requests.get(url)
            filename = url.split("/")[-1]
            filepath = os.path.join(os.getcwd(), "data/raw", filename)
            with open(filepath, 'w') as f:
                f.write(response.text)


    
    def run_scraper(self):
        self.open_browser()
        relevant_links = self.gather_hrefs_by_pattern(self.pattern)
        self.save_raw_data_locally(relevant_links)
    
    def close_browser(self):
        self.driver.quit()

if __name__=='__main__':
    print('Scraper loadded as main')
    test_scp = Met_Scraper()
    test_scp.run_scraper()


