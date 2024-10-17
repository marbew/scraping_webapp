from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
import os

# Email configuration
sender_email = ''
recipient_email = ''
smtp_server = 'smtp.example.com'
smtp_port = 587
email_password = ''

# URL to scrape
url = 'https://webpage_to_scrape.example.com'

# File to store the previous Controlled Total content value
prev_file = '~/prev.txt'

# Function to send email
def send_email(new_content):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, email_password)
        message = f'Subject: Content Updated\n\nNew value is: {new_content}'
        server.sendmail(sender_email, recipient_email, message)

# Function to scrape the content value
def get_cont_value():
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless
    chrome_options.add_argument('--no-sandbox')  # Required for some environments
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    driver_service = Service('/usr/bin/chromedriver')  # Update this path if necessary
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)  # Add options here
    driver.get(url)

    try:
        # Wait for the span element containing the content value to be present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='text-secondary-4 dark:text-secondaryDark-2 font-semibold text-sm']"))
        )
        cont_value = element.text.strip()  # Remove whitespace
        print(f"Content Value Found: {cont_value}")  # Debugging output
    except Exception as e:
        print(f"Error finding the content value: {e}")
        cont_value = None
    finally:
        driver.quit()

    return cont_value

# Main function to compare and update content value
def main():
    print('Script started.')

    current_content = get_cont_value()
    if not current_content:
        print('Failed to retrieve content value.')
        return

    previous_content = None

    # Read the previous content from the file if it exists
    if os.path.exists(prev_file):
        with open(prev_file, 'r') as file:
            previous_content = file.read().strip()

    if current_content != previous_content:
        print(f'content updated from {previous_content} to {current_content}. Sending email...')
        send_email(current_content)

        # Update the stored content value
        with open(prev_file, 'w') as file:
            file.write(current_content)
    else:
        print('No change in Controlled Total content.')

if __name__ == "__main__":
    main()
