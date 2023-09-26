import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from fake_useragent import UserAgent


class WebScraper:
    def __init__(self, url):
        self.__BASE_URL = url

        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        # To avoid bot detections
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        ua = UserAgent()
        user_agent = ua.random
        self.options.add_argument(f'user-agent={user_agent}')

    def fetch_page_content(self, url):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        driver.get(url)
        time.sleep(3)
        result = driver.page_source
        driver.close()
        return result

    def split_content_into_jobs(self, content):
        job_list = []

        soup = BeautifulSoup(content, 'html.parser')
        jobs = soup.find_all("li", {"class": "css-5lfssm eu4oa1w0"})
        for job_html in jobs:
            job_soup = BeautifulSoup(job_html.prettify(), 'html.parser')

            # See if there is a business behind this poster, otherwise it is most likely an ad
            company = job_soup.find("span", {"class": "companyName"})
            if not company:
                continue

            # Just save it as raw HTML for now, we can run a separate translation function on it later
            job_list.append(job_html.prettify())

        return job_list

    def main(self):
        content = self.fetch_page_content(f'{self.__BASE_URL}')
        html_jobs = self.split_content_into_jobs(content)
        return html_jobs

