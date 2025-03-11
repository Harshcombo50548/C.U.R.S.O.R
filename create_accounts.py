#                                     WELCOME TO
#
#  .d8888b.      888     888     8888888b.       .d8888b.       .d88888b.      8888888b.  
# d88P  Y88b     888     888     888   Y88b     d88P  Y88b     d88P" "Y88b     888   Y88b 
# 888    888     888     888     888    888     Y88b.          888     888     888    888 
# 888            888     888     888   d88P      "Y888b.       888     888     888   d88P 
# 888            888     888     8888888P"          "Y88b.     888     888     8888888P"  
# 888    888     888     888     888 T88b             "888     888     888     888 T88b   
# Y88b  d88P d8b Y88b. .d88P d8b 888  T88b  d8b Y88b  d88P d8b Y88b. .d88P d8b 888  T88b  
#  "Y8888P"  Y8P  "Y88888P"  Y8P 888   T88b Y8P  "Y8888P"  Y8P  "Y88888P"  Y8P 888   T88b 
#
#        {Creating User Registrations with Scripted Optimization and Replication}

import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import string
import yaml
import os
from selenium.common.exceptions import TimeoutException

class AccountGenerator:
    def __init__(self, config_path="config.yaml"):
        self.load_config(config_path)
        self.setup_driver()
        self.accounts = []

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_driver(self):
        # Launch Chrome with remote debugging and disable GPU to mitigate errors
        subprocess.Popen([
            "google-chrome",
            "--remote-debugging-port=9222",
            "--user-data-dir=/tmp/chrome-profile",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-gpu",  # Added to mitigate GPU stall errors
            "https://www.cursor.com/"
        ])
        time.sleep(15)  # Increased wait for Chrome to fully load the page and render JS

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        self.driver = webdriver.Chrome(options=chrome_options)
        print("Connected to automated Chrome instance")
        self.driver.save_screenshot("initial_page.png")

    def generate_random_string(self, length):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def create_gmail(self):
        first_name = self.generate_random_string(8)
        last_name = self.generate_random_string(8)
        username = f"{first_name}{last_name}{random.randint(100, 999)}"
        password = self.generate_random_string(12)
        return {
            "email": f"{username}@gmail.com",
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }

    def simulate_human_typing(self, element, text):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()
        time.sleep(random.uniform(0.5, 1.5))
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(0.5, 1))

    def simulate_human_mouse(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(element, random.randint(-10, 10), random.randint(-10, 10))
        actions.pause(random.uniform(0.5, 1.5)).perform()
        time.sleep(random.uniform(0.3, 0.7))

    def create_account(self):
        try:
            credentials = self.create_gmail()

            # Navigate to Sign in
            print("Navigating to Sign in...")
            try:
                # Wait for the element using a more robust XPath
                sign_in_link = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='Sign in' and @href='/api/auth/login']"))
                )
            except TimeoutException:
                print("Primary Sign in XPath failed, trying fallback...")
                try:
                    sign_in_link = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='Sign in']"))
                    )
                except TimeoutException:
                    print("Fallback XPath failed, navigating directly to sign-in URL...")
                    self.driver.get("https://www.cursor.com/api/auth/login")
                    time.sleep(random.uniform(2, 4))
                    print(f"Direct navigation to sign-in URL: {self.driver.current_url}")
                    self.driver.save_screenshot("sign_in_page.png")

            if "sign-in" not in self.driver.current_url.lower():
                self.simulate_human_mouse(sign_in_link)
                sign_in_link.click()
                print("Clicked Sign in")
                time.sleep(random.uniform(2, 4))
                print(f"Current URL after Sign in click: {self.driver.current_url}")
                self.driver.save_screenshot("sign_in_page.png")

            # Navigate to Sign up
            print("Navigating to Sign up...")
            try:
                sign_up_link = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'rt-Text') and normalize-space(text())='Sign up']"))
                )
            except TimeoutException:
                print("Primary Sign up XPath failed, trying fallback...")
                sign_up_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='Sign up']"))
                )
            self.simulate_human_mouse(sign_up_link)
            sign_up_link.click()
            print("Clicked Sign up")
            time.sleep(random.uniform(2, 4))
            print(f"Current URL after Sign up click: {self.driver.current_url}")
            self.driver.save_screenshot("sign_up_page.png")

            # Random scroll to mimic human browsing
            self.driver.execute_script("window.scrollBy(0, {0});".format(random.randint(50, 150)))
            time.sleep(random.uniform(1, 2))

            # Fill signup form
            first_name_field = self.driver.find_element(By.NAME, "first_name")
            self.simulate_human_mouse(first_name_field)
            self.simulate_human_typing(first_name_field, credentials['first_name'])
            print("Filled first name")

            last_name_field = self.driver.find_element(By.NAME, "last_name")
            self.simulate_human_mouse(last_name_field)
            self.simulate_human_typing(last_name_field, credentials['last_name'])
            print("Filled last name")

            email_field = self.driver.find_element(By.NAME, "email")
            self.simulate_human_mouse(email_field)
            self.simulate_human_typing(email_field, credentials['email'])
            print("Filled email")

            # Pause for manual Cloudflare verification (accounting for two prompts)
            print("Pausing for manual Cloudflare verification (120s total, check both prompts if needed)...")
            self.driver.save_screenshot("pre_submit.png")
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            self.simulate_human_mouse(submit_button)
            time.sleep(random.uniform(0.7, 1.5))
            submit_button.click()
            print("Clicked submit")
            time.sleep(5)
            print(f"Current URL after submit: {self.driver.current_url}")
            self.driver.save_screenshot("post_submit.png")

            # Wait for Cloudflare widget and allow manual intervention
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, "cf-turnstile"))
                )
                print("Cloudflare Turnstile widget detected (first prompt)")
                self.driver.save_screenshot("turnstile_detected_1.png")

                print("Please manually check the first Cloudflare verification box (60s)...")
                time.sleep(60)
                self.driver.save_screenshot("post_first_verification.png")

                # Check for second prompt
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.ID, "cf-turnstile"))
                    )
                    print("Second Cloudflare Turnstile widget detected")
                    self.driver.save_screenshot("turnstile_detected_2.png")

                    print("Please manually check the second Cloudflare verification box (60s)...")
                    time.sleep(60)
                    self.driver.save_screenshot("post_second_verification.png")
                except TimeoutException:
                    print("No second Cloudflare prompt detected, proceeding...")

                print(f"URL after manual verification: {self.driver.current_url}")

                if "verify" in self.driver.current_url.lower() or "cloudflare" in self.driver.current_url.lower():
                    print("Manual verification did not resolve. Aborting...")
                    return False

                error_message = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Can’t verify the user is human')]")
                if error_message:
                    print("Error: Can’t verify the user is human. Aborting...")
                    return False

            except TimeoutException as e:
                print(f"Timeout waiting for Cloudflare widget: {str(e)}")
                self.driver.save_screenshot("no_cloudflare.png")
                return False
            except Exception as e:
                print(f"Error during Cloudflare verification: {e}")
                self.driver.save_screenshot("cloudflare_error.png")
                return False

            # Proceed to Google OAuth
            google_button = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Continue with Google')]"))
            )
            self.simulate_human_mouse(google_button)
            time.sleep(random.uniform(0.7, 1.5))
            google_button.click()
            print("Clicked Google OAuth")
            time.sleep(5)

            self.accounts.append({
                "email": credentials['email'],
                "password": credentials['password'],
                "created_at": time.ctime()
            })
            return True

        except TimeoutException as e:
            print(f"Timeout during navigation or form filling: {str(e)}")
            self.driver.save_screenshot("error.png")
            return False
        except Exception as e:
            print(f"Error creating account: {e}")
            self.driver.save_screenshot("error.png")
            return False

    def save_accounts(self):
        with open("accounts.yaml", "a") as f:
            yaml.dump(self.accounts, f)

    def run(self):
        for _ in range(self.config['account_count']):
            if self.create_account():
                print(f"Successfully created account {_ + 1}/{self.config['account_count']}")
            else:
                print(f"Failed to create account {_ + 1}")
            time.sleep(random.uniform(5, 10))
        
        self.save_accounts()
        self.driver.quit()

if __name__ == "__main__":
    generator = AccountGenerator()
    generator.run()