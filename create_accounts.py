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
import requests  # For making HTTP requests to the temp mail service
import re

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

    def get_temp_email(self):
        """Get a temporary email address from mail.tm service."""
        try:
            # Create a random domain name from the available domains at mail.tm
            domains_response = requests.get("https://api.mail.tm/domains")
            domains = domains_response.json()["hydra:member"]
            domain = domains[0]["domain"]  # Get the first available domain
            
            # Generate a random username
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            email = f"{username}@{domain}"
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # Create the account on mail.tm
            account_data = {
                "address": email,
                "password": password
            }
            response = requests.post("https://api.mail.tm/accounts", json=account_data)
            
            if response.status_code == 201:
                # Log in to get the auth token
                login_data = {
                    "address": email,
                    "password": password
                }
                token_response = requests.post("https://api.mail.tm/token", json=login_data)
                self.temp_mail_token = token_response.json()["token"]
                print(f"Successfully created temporary email: {email}")
                
                # Store temp mail credentials for later use
                self.temp_mail_credentials = {
                    "email": email,
                    "password": password,
                    "token": self.temp_mail_token
                }
                
                return email
            else:
                print(f"Error creating temp mail: {response.text}")
                # Fallback to a different temp mail service
                return self.get_tempmail_fallback()
        except Exception as e:
            print(f"Error creating temporary email: {str(e)}")
            # Fallback to a different service
            return self.get_tempmail_fallback()

    def get_tempmail_fallback(self):
        """Fallback method using temp-mail.org."""
        try:
            # Generate random username
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            
            # Use temp-mail.org (note: their API may require registration for full access)
            email = f"{username}@tmpmail.net"
            print(f"Using fallback temporary email: {email}")
            return email
        except Exception as e:
            print(f"Error with fallback email: {str(e)}")
            # If all fails, generate a dummy email - the user will need to manually check
            random_name = ''.join(random.choices(string.ascii_lowercase, k=8))
            return f"{random_name}@example.com"

    def get_verification_code(self, email):
        """Get the verification code from the temporary email."""
        max_attempts = 10
        delay_seconds = 12
        
        headers = {}
        if hasattr(self, 'temp_mail_token') and self.temp_mail_token:
            headers = {"Authorization": f"Bearer {self.temp_mail_token}"}
        
        # Try to fetch emails multiple times with a delay
        for attempt in range(max_attempts):
            try:
                print(f"Checking for verification email (attempt {attempt+1}/{max_attempts})...")
                
                if "@mail.tm" in email or "@tmpmail.net" in email:
                    # For mail.tm service
                    response = requests.get("https://api.mail.tm/messages", headers=headers)
                    if response.status_code == 200:
                        messages = response.json()["hydra:member"]
                        
                        for message in messages:
                            if "verification" in message["subject"].lower() or "code" in message["subject"].lower():
                                # Get the full message content
                                msg_id = message["id"]
                                msg_response = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers)
                                
                                if msg_response.status_code == 200:
                                    full_message = msg_response.json()
                                    # Get HTML content
                                    html_content = full_message.get("html", "")
                                    # Extract code from the email content
                                    code = self.extract_code_from_email(html_content)
                                    if code:
                                        print(f"Found verification code: {code}")
                                        return code
                else:
                    # For temp-mail.org or other services
                    # Use their API endpoints - will require specific implementation based on the service
                    pass
                    
                # If we didn't find a code, wait and retry
                print(f"No verification code found yet. Waiting {delay_seconds} seconds...")
                time.sleep(delay_seconds)
                
            except Exception as e:
                print(f"Error checking for verification code: {str(e)}")
                time.sleep(delay_seconds)
        
        print("Failed to get verification code after multiple attempts")
        return None

    def extract_code_from_email(self, email_body):
        """Extract the verification code from the email body."""
        try:
            # Try different patterns for code extraction
            
            # Pattern 1: Look for digits in specific lengths (4-8 digits is common for verification codes)
            if isinstance(email_body, str):
                # Look for 6-digit code (most common)
                six_digit_pattern = r'\b\d{6}\b'
                matches = re.findall(six_digit_pattern, email_body)
                if matches:
                    return matches[0]
                
                # Try 4-digit code
                four_digit_pattern = r'\b\d{4}\b'
                matches = re.findall(four_digit_pattern, email_body)
                if matches:
                    return matches[0]
                
                # Look for code that might be formatted with spaces or hyphens
                formatted_code_pattern = r'\b\d[\d\s-]{2,10}\d\b'
                matches = re.findall(formatted_code_pattern, email_body)
                if matches:
                    # Remove any spaces or hyphens
                    return re.sub(r'[\s-]', '', matches[0])
                
                # Look for code after specific phrases
                phrases = [
                    r'verification code[^\d]*(\d+)',
                    r'verification code is[^\d]*(\d+)',
                    r'your code is[^\d]*(\d+)',
                    r'your code:[^\d]*(\d+)',
                    r'code:[^\d]*(\d+)'
                ]
                
                for pattern in phrases:
                    matches = re.search(pattern, email_body.lower())
                    if matches:
                        return matches.group(1)
            
            # If all automated extraction methods fail, show a snippet of the email
            # so we can see the format for debugging
            print("Couldn't automatically extract code. Email preview:")
            preview = email_body[:200] + "..." if len(email_body) > 200 else email_body
            print(preview)
            
            # As a last resort, ask the user to input the code manually
            manual_code = input("Please check the email and enter the verification code manually: ")
            if manual_code.strip():
                return manual_code.strip()
            
        except Exception as e:
            print(f"Error extracting code: {str(e)}")
        
        # If all else fails, return None
        return None

    def create_account(self):
        try:
            credentials = self.create_gmail()
            credentials['email'] = self.get_temp_email()  # Use temporary email

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

            # Wait for email verification
            print("Waiting for email verification code...")
            verification_code = None
            for _ in range(10):  # Retry for a limited number of times
                verification_code = self.get_verification_code(credentials['email'])
                if verification_code:
                    break
                time.sleep(10)  # Wait before retrying

            if not verification_code:
                print("Failed to retrieve verification code. Aborting...")
                return False

            # Enter verification code
            verification_code_field = self.driver.find_element(By.NAME, "verification_code")
            self.simulate_human_typing(verification_code_field, verification_code)
            print("Entered verification code")

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
        """Save the created accounts to a YAML file."""
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"accounts_{timestamp}.yaml"
        
        # Format accounts with readable headings
        formatted_accounts = []
        for i, account in enumerate(self.accounts, 1):
            formatted_account = {
                f"Account {i}": {
                    "email": account["email"],
                    "password": account["password"],
                    "created_at": account["created_at"]
                }
            }
            formatted_accounts.append(formatted_account)
        
        # Also keep the original format for accounts.yaml
        with open("accounts.yaml", "w") as f:
            yaml.dump(self.accounts, f, default_flow_style=False)
        
        # Create the formatted version
        with open(filename, "w") as f:
            yaml.dump(formatted_accounts, f, default_flow_style=False)
        
        print(f"Accounts saved to {filename} and accounts.yaml")
        
        # Print a summary to the console
        print("\n=== ACCOUNT SUMMARY ===")
        for i, account in enumerate(self.accounts, 1):
            print(f"Account {i}:")
            print(f"  Email: {account['email']}")
            print(f"  Password: {account['password']}")
            print(f"  Created: {account['created_at']}")
            print("------------------------")

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