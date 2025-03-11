#!/usr/bin/env python3
"""
Cursor.com Account Creator
This script automates the process of creating accounts on cursor.com using
temporary email services.
"""

import subprocess
import time
import random
import string
import yaml
import os
import logging
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import requests
import undetected_chromedriver as uc  # For bypassing detection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler("cursor_account_creation.log")  # Output to file
    ]
)
logger = logging.getLogger(__name__)

class CursorAccountCreator:
    """Class to handle the creation of Cursor.com accounts"""
    
    def __init__(self, output_file="accounts.yaml"):
        """Initialize the account creator with configuration"""
        self.output_file = output_file
        # Check if output file exists, if not create it with empty accounts list
        if not os.path.exists(output_file):
            with open(output_file, 'w') as file:
                yaml.dump({"accounts": []}, file)
        
        # Initialize browser
        self.browser = None
        self.email = None
        self.password = None
        
    def setup_browser(self):
        """Set up the browser with undetected chromedriver"""
        logger.info("Setting up browser...")
        
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        # Add additional options as needed
        
        # Use undetected_chromedriver to avoid detection
        self.browser = uc.Chrome(options=options)
        logger.info("Browser setup complete")
        
    def generate_password(self, length=12):
        """Generate a random secure password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def get_temp_email(self):
        """Generate a temporary email using 1secmail API"""
        logger.info("Generating temporary email...")
        
        response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        if response.status_code == 200:
            self.email = response.json()[0]
            logger.info(f"Temporary email generated: {self.email}")
            return self.email
        else:
            logger.error("Failed to generate temporary email")
            raise Exception("Failed to generate temporary email")
    
    def check_for_verification_email(self, max_attempts=30, delay=10):
        """Check for verification email in the temporary mailbox"""
        logger.info(f"Checking for verification email at {self.email}...")
        
        # Parse the email address
        username, domain = self.email.split('@')
        
        for attempt in range(max_attempts):
            logger.info(f"Checking for emails (attempt {attempt+1}/{max_attempts})...")
            
            # Get mailbox messages
            response = requests.get(
                f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
            )
            
            if response.status_code == 200:
                messages = response.json()
                
                # Look for verification email
                for message in messages:
                    if "cursor" in message.get("subject", "").lower() or "verification" in message.get("subject", "").lower():
                        logger.info(f"Verification email found: {message['subject']}")
                        
                        # Get the email content
                        email_id = message["id"]
                        email_response = requests.get(
                            f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={email_id}"
                        )
                        
                        if email_response.status_code == 200:
                            email_content = email_response.json()
                            # Extract verification code using regex
                            # This pattern might need adjustment based on the actual email format
                            match = re.search(r'verification code[:\s]*([0-9]{4,6})', 
                                             email_content.get("body", ""), re.IGNORECASE)
                            
                            if match:
                                verification_code = match.group(1)
                                logger.info(f"Verification code found: {verification_code}")
                                return verification_code
                            else:
                                logger.warning("Could not extract verification code from email")
            
            logger.info(f"No verification email yet. Waiting {delay} seconds...")
            time.sleep(delay)
        
        logger.error("Failed to receive verification email after maximum attempts")
        raise Exception("Verification email not received")
    
    def create_account(self):
        """Create a new Cursor.com account"""
        try:
            # Setup browser if not already done
            if not self.browser:
                self.setup_browser()
            
            # Generate temporary email and password
            self.get_temp_email()
            self.password = self.generate_password()
            
            logger.info(f"Creating account with email: {self.email} and password: {self.password}")
            
            # Navigate to cursor.com
            logger.info("Navigating to cursor.com...")
            self.browser.get("https://cursor.com")
            
            # Wait for page to load
            time.sleep(2)
            
            # Find and click the sign in button
            logger.info("Looking for sign in button...")
            signin_button = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign In')]"))
            )
            signin_button.click()
            logger.info("Clicked sign in button")
            
            # Wait for sign in page and find sign up link
            logger.info("Looking for sign up option...")
            signup_link = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign up')]"))
            )
            signup_link.click()
            logger.info("Clicked sign up option")
            
            # Wait for sign up form
            logger.info("Filling out sign up form...")
            
            # Enter email
            email_input = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
            )
            email_input.clear()
            email_input.send_keys(self.email)
            logger.info("Entered email")
            
            # Submit email
            email_input.submit()
            logger.info("Submitted email")
            
            # Enter password
            password_input = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
            )
            password_input.clear()
            password_input.send_keys(self.password)
            logger.info("Entered password")
            
            # Submit password
            password_input.submit()
            logger.info("Submitted password")
            
            # Get verification code from email
            logger.info("Waiting for verification email...")
            verification_code = self.check_for_verification_email()
            
            # Enter verification code
            verification_input = WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@aria-label, 'verification') or contains(@placeholder, 'code')]"))
            )
            verification_input.clear()
            verification_input.send_keys(verification_code)
            logger.info("Entered verification code")
            
            # Submit verification code
            verification_input.submit()
            logger.info("Submitted verification code")
            
            # Wait for account creation to complete
            time.sleep(5)
            
            # Save account details
            self.save_account()
            
            logger.info("Account creation completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error during account creation: {str(e)}")
            # Take screenshot if browser is available
            if self.browser:
                screenshot_path = f"error_screenshot_{int(time.time())}.png"
                self.browser.save_screenshot(screenshot_path)
                logger.info(f"Error screenshot saved to {screenshot_path}")
            return False
            
        finally:
            # Close browser after completion or error
            if self.browser:
                logger.info("Closing browser...")
                self.browser.quit()
    
    def save_account(self):
        """Save account credentials to YAML file"""
        logger.info(f"Saving account details to {self.output_file}...")
        
        # Load existing accounts
        with open(self.output_file, 'r') as file:
            data = yaml.safe_load(file)
        
        # Add new account
        account_data = {
            "email": self.email,
            "password": self.password,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if not data:
            data = {"accounts": []}
        elif "accounts" not in data:
            data["accounts"] = []
            
        data["accounts"].append(account_data)
        
        # Save updated data
        with open(self.output_file, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
        
        logger.info("Account details saved successfully")

def main():
    """Main function to run the account creator"""
    logger.info("Starting Cursor.com account creation process")
    
    creator = CursorAccountCreator()
    success = creator.create_account()
    
    if success:
        logger.info("Account creation completed successfully!")
    else:
        logger.error("Account creation failed.")
    
if __name__ == "__main__":
    main()
