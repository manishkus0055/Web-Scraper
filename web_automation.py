# THIS FILE IS FOR ACTUAL AUTOMATING THE BROWSER AND DIFFERENT KIND OF LOGIN/REGISTER METHODS ON A SITE
import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException

class WebAutomation:
    def __init__(self, use_proxy=False, proxy_address=None):
        """
        Initialize the WebAutomation class with optional proxy support.
        Args:
            use_proxy (bool): Whether to use a proxy.
            proxy_address (str): Proxy address in the format "IP:PORT".
        """

        options = Options()

        # Run the browser in headless mode
        #options.add_argument("headless")    

        # Disable certain features that indicate the browser is being controlled by automation
        options.add_argument("--disable-blink-features=AutomationControlled")  

        # This option is used to prevent issues related to shared memory in Docker containers or environments
        # where /dev/shm is not available or has limited space.
        options.add_argument("--disable-dev-shm-usage") 

        # This option disables the sandboxing feature of the browser, which can help in environments
        # where the sandbox may cause issues, such as in certain Docker configurations.
        options.add_argument("--no-sandbox")

        # Disguise selenium
        options.set_preference("dom.webdriver.enable", False)  

        # Prevent detection 
        options.set_preference("useAutomationExtension", False)

        # Use random User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        options.set_preference("general.useragent.override", random.choice(user_agents))

        # Basic settings
        options.page_load_strategy = "normal"
        options.unhandled_prompt_behavior = "accept and notify"

        ## Set up proxy if enabled
        #if use_proxy and proxy_address:
        #    self.proxy_setting(options, proxy_address)

        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def proxy_setting(self, options, proxy_address):
        """
        Set up a proxy for the WebDriver.
        Args:
            options (Options): FirefoxOptions instance.
            proxy_address (str): Proxy address in the format "IP:PORT".
        """
        proxy = Proxy({
            "proxyType": ProxyType.MANUAL,
            "httpProxy": proxy_address,
            "sslProxy": proxy_address,
            "socksProxy": proxy_address,
            "socksVersion":5,
            "noProxy": ""   # Use an empty string for no exceptions
        })

        # Attach the proxy to the options
        options.proxy = proxy
        print(f"Proxy set to {proxy_address}")

class AutomateWebApp(WebAutomation):
    def instagram(self, url, userid=None, password=None, id=None):
        """
        Open a Instagram URL
        Args:
            url: Instagram login URL
            userid: Username for login
            password: Password for login
            id: ID of an account for scraping
        Returns:
            The page source after all operations
        """
        elements_to_be_found = {
            "body": "body", # By.TAG_NAME
            "username": "username", # By.NAME
            "password": "password", # By.NAME
            "submit_button": "._acap > div:nth-child(1)",   # By.CSS_SELECTOR
            "save_info_button": "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/section/div/button",   # By.XPATH
            "click_cearch_button": "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[2]/span/div/a/div/div[2]/div/div/span/span",   # By.XPATH
            "input_in_search": "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/input",   # By.XPATH
            "click_to_the_id": "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/a[1]/div[1]/div/div" # By.XPATH
        }

        try:
            self.driver.get(url)

            # Wait for the page to load
            try:
                WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, elements_to_be_found["body"])))

                # Login
                try:
                    # Check if username and password elements exists
                    username_elem = WebDriverWait(self.driver, 6).until(expected_conditions.presence_of_element_located((By.NAME, elements_to_be_found["username"])))
                    password_elem = WebDriverWait(self.driver, 6).until(expected_conditions.presence_of_element_located((By.NAME, elements_to_be_found["password"])))
                    # Input your initials
                    username_elem.send_keys(userid)
                    password_elem.send_keys(password)

                    # Find and click submit button
                    submit_button = WebDriverWait(self.driver, 6).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, elements_to_be_found["submit_button"])))
                    submit_button.click()

                    # Click save info button or not now button
                    WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, elements_to_be_found["save_info_button"]))).click()

                    # Wait sometime until page is loaded properly
                    time.sleep(10)

                    # Search the id you want to find and get into it
                    try:
                        # Click Search Button
                        click_cearch_button = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, elements_to_be_found["click_cearch_button"])))
                        click_cearch_button.click()

                        # Input in search
                        input_in_search = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, elements_to_be_found["input_in_search"])))
                        input_in_search.click()
                        input_in_search.send_keys(id)

                        # Click the first id probably == id you are looking for
                        click_to_the_id = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, elements_to_be_found["click_to_the_id"])))
                        click_to_the_id.click()

                        ## Scroll the pag to load more content
                        #for _ in range(60):
                        #    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        #    time.sleep(random.uniform(2, 4)) # Random wait between scolls
                    
                    except (NoSuchElementException, TimeoutException) as e:
                        print(f"No Search button found or elements not accessible: {str(e)}")
                    
                    # Wait additional time for the new page to fully load
                    time.sleep(random.uniform(2, 4))

                    # Wait for body of new page
                    WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.TAG_NAME, elements_to_be_found["body"])))

                    print(f"Current URL after operation: {self.driver.current_url}")

                except (NoSuchElementException, TimeoutException) as e:
                    print(f"No Login element found or elements not accessible: {str(e)}")
                
            except WebDriverException as e:
                print(f"WebDriverExceptions while waiting for page load: {str(e)}")
                return None
            
            # Get the page source after all the operations are complete
            return self.driver.page_source
        
        except WebDriverException as e:
            print(f"WebDriverException: {str(e)}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()