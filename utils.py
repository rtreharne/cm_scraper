from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import getpass
import time
import os

class CanvasSession:
    def __init__(self):
        # Get username and password from user
        self.username = input("Input your MWS username: ")
        self.password = getpass.getpass("Input your MWS password: ")
        
        # Configure webdriver
        
        # Get the current directory
        current_dir = os.getcwd()

        # Append the file name to the current directory
        CHROMEDRIVER_PATH = os.path.join(current_dir, 'chromedriver.exe')

        service = Service(executable_path=CHROMEDRIVER_PATH)
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(service=service, options=options)
        
        # Login
        self.browser.get('https://canvas.liverpool.ac.uk')
        
        username_input = self.browser.find_element(By.XPATH, "//input[@name='UserName']")
        password_input = self.browser.find_element(By.XPATH, "//input[@name='Password']")

        # Get submit button by text "LOG IN"
        submit_button = self.browser.find_element(By.XPATH, "//span[contains(text(),'Sign in')]")
        
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        
        submit_button.click()
        
        # Wait for 10 seconds
        print("wait ...")
        time.sleep(10)
        
        # Find all elements with the class "verification-code"
        elements = self.browser.find_elements(By.CLASS_NAME, "verification-code")
        
        # Print the text content of each element
        for element in elements:
            print("Verification code for DUO")
            print(element.text)

        # Countdown loop
        for i in range(20, 0, -1):
            print("You have {} seconds to enter your verification code.".format(i), end="\r")
            time.sleep(1)
        
        # Confirm trust browser
        try:
            self.browser.find_element(By.ID, "trust-browser-button").click()
            print("")
            print("Login Success.")
        except:
            print("")
            print("Login Failure")


import tempfile
import getpass
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class CMSession:
    def __init__(self):
        self.username = input("Input your MWS username: ")
        self.password = getpass.getpass("Input your MWS password: ")

        # 🔧 Create a temporary Firefox profile directory
        profile_dir = tempfile.mkdtemp()
        profile = FirefoxProfile(profile_dir)

        # 🚫 Turn off notifications (optional)
        profile.set_preference("dom.webnotifications.enabled", False)
        profile.set_preference("dom.push.enabled", False)
        profile.update_preferences()

        # Set up Firefox options and attach the profile
        options = Options()
        # options.add_argument("-headless")  # Optional headless mode
        options.profile = profile  # ✅ CORRECT way to assign the profile

        # Launch browser
        self.browser = webdriver.Firefox(service=Service(), options=options)

        # The rest of your code...
        self.browser.get('https://liverpool-curriculum.worktribe.com/')
        print("wait ...")
        time.sleep(5)

        username_input = self.browser.find_element(By.XPATH, "//input[@id='username']")
        password_input = self.browser.find_element(By.XPATH, "//input[@id='password']")
        submit_button = self.browser.find_element(By.CLASS_NAME, "form-button")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        submit_button.click()

        print("wait ...")
        time.sleep(5)

        elements = self.browser.find_elements(By.CLASS_NAME, "verification-code")
        for element in elements:
            print("Verification code for DUO")
            print(element.text)

        for i in range(20, 0, -1):
            print(f"You have {i} seconds to enter your verification code.", end="\r")
            time.sleep(1)

        try:
            self.browser.find_element(By.ID, "trust-browser-button").click()
            print("\nLogin Success.")
        except:
            print("\nLogin Failure")


if __name__ == "__main__":
    session = CMSession()
    