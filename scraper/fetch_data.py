import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains


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
        ua = UserAgent(os='windows')
        user_agent = ua.random
        self.options.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def fetch_page_content(self, url):
        self.driver.get(url)
        time.sleep(3)
        result = self.driver.page_source

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

            # Get the job name
            title = job_soup.find('span')

            # Find the link to click to expand the job info
            link = self.driver.find_element(By.PARTIAL_LINK_TEXT, f'{str(title.text).strip()}')
            action = ActionChains(self.driver)
            action.click(on_element=link)
            action.perform()
            # print(f"Clicked on job {str(title.text).strip()}")
            time.sleep(5)

            # Just save it as raw HTML for now, we can run a separate translation function on it later
            job_list.append(self.driver.page_source)

        return job_list

    def main(self):
        content = self.fetch_page_content(f'{self.__BASE_URL}')
        html_jobs = self.split_content_into_jobs(content)
        self.driver.close()
        return html_jobs

