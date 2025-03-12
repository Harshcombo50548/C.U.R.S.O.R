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

import time
import random
import requests
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

def human_delay(min_sec=1, max_sec=3):
    # Random wait between actions
    time.sleep(random.uniform(min_sec, max_sec))

def get_temp_email():
    # Get disposable email from mail.tm
    try:
        # Find available email domains
        domains = requests.get("https://api.mail.tm/domains").json()['hydra:member']
        domain = domains[0]['domain']
        
        # Generate random email credentials
        email = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=12))}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Create mail.tm account
        acc_response = requests.post("https://api.mail.tm/accounts", json={
            "address": email, 
            "password": password
        })
        
        # Get auth token
        token = requests.post("https://api.mail.tm/token", json={
            "address": email,
            "password": password
        }).json()['token']

        return {"email": email, "token": token}
        
    except Exception as e:
        print(f"Email error: {e}")
        return None

def get_verification_code(email, auth_token):
    # Check mailbox for verification code
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    for _ in range(10):
        try:
            messages = requests.get("https://api.mail.tm/messages", headers=headers).json()['hydra:member']
            if messages:
                text = requests.get(f"https://api.mail.tm/messages/{messages[0]['id']}", 
                                  headers=headers).json().get('text', '')
                code = ''.join(filter(str.isdigit, text))
                if code: return code[:6]
            
            time.sleep(5)
        except:
            time.sleep(10)
    return None

def main():
    # Browser setup
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Start Chrome
    driver = Chrome(
        executable_path=ChromeDriverManager().install(),
        options=options,
        suppress_welcome=True,
        headless=False,
        version_main=134
    )
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    wait = WebDriverWait(driver, 25)
    actions = ActionChains(driver)
    
    try:
        # Start process
        driver.get("https://cursor.com")
        human_delay(2,4)
        input("\n>>> Go to signup page in browser, then press Enter...")
        
        # Email handling
        temp_acc = get_temp_email()
        if not temp_acc: return
        
        # Enter email
        email_field = wait.until(EC.element_to_be_clickable((By.NAME, 'email')))
        actions.move_to_element(email_field).pause(random.uniform(0.5,1.5)).perform()
        
        # Type email with human-like errors
        for char in temp_acc['email']:
            if random.random() < 0.1:  # Simulate typos
                email_field.send_keys(random.choice(string.ascii_lowercase))
                time.sleep(random.uniform(0.2,0.4))
                email_field.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1,0.3))
                
            email_field.send_keys(char)
            time.sleep(max(random.gauss(0.15,0.05), 0.05))
            
            if random.random() < 0.07:  # Pause to "check" input
                time.sleep(random.uniform(0.8,1.5))
                actions.move_by_offset(random.randint(-5,5), random.randint(-5,5)).perform()
        
        # Submit email
        input("\n>>> Complete Cloudflare checks and press Enter...")
        actions.send_keys("\ue007").perform()
        
        # Password handling
        input("\n>>> Complete checks and press Enter for password...")
        password = f"CursorAI@{random.randint(1000,9999)}"
        for char in password:
            wait.until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(char)
            time.sleep(random.uniform(0.05,0.2))
        
        human_delay()
        
        # Verification code
        input("\n>>> Press Enter to check for code...")
        code = get_verification_code(temp_acc['email'], temp_acc['token'])
        if not code: return
        
        human_delay(2,3)
        wait.until(EC.visibility_of_element_located((By.ID, 'verification-container')))
        
        # Enter code
        code_field = wait.until(EC.element_to_be_clickable((By.NAME, 'code')))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", code_field)
        
        for char in code:
            if random.random() < 0.15:  # Simulate code typos
                code_field.send_keys(random.choice(string.digits))
                time.sleep(random.uniform(0.1,0.3))
                code_field.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1,0.2))
                
            code_field.send_keys(char)
            time.sleep(random.uniform(0.1,0.4))
            
            if random.random() < 0.2:  # Random mouse movements
                actions.move_to_element(code_field).move_by_offset(random.randint(-5,5), random.randint(-5,5)).perform()
        
        print("\nAccount created!")
        human_delay(5,7)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()


