import re
import html2text
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def get_html_content(url, element_name: None, by=By.CLASS_NAME, time_wait: int = 10):
    print("🚀 Starting the web scraping process...")

    # Set up the Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Set up the Chrome driver
    service = Service()  # Update with the correct path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the URL
        print(f"🌐 Opening the URL: {url}")
        driver.get(url)
        if element_name:
            print(f"⌛ Waiting for the element: {element_name}")
            WebDriverWait(driver, time_wait).until(EC.presence_of_element_located((by, element_name)))
        else:
            print(f"⌛ Waiting for {time_wait} seconds")
            WebDriverWait(driver, time_wait)

        # Get the page source
        print("📄 Retrieving the page source...")
        html_content = driver.page_source
    finally:
        # Close the driver
        print("🛑 Closing the web driver...")
        driver.quit()

    print("✅ Web scraping process completed!")
    return html_content

def get_markdown_data(url, element_name: None, by=By.CLASS_NAME, time_wait: int = 10) -> str:
    print("📝 Converting HTML content to Markdown...")
    html_content = get_html_content(url, element_name, by, time_wait)
    markdown_content = convert_html_to_markdown(html_content)
    print("✅ Conversion to Markdown completed!")
    return markdown_content

def convert_html_to_markdown(html_content):
    # Create an html2text object
    h = html2text.HTML2Text()
    
    # Ignore links in the conversion if needed
    h.ignore_links = False
    
    # Remove image data from HTML content
    html_content = re.sub(r'<img[^>]*>', '', html_content)
    
    # Remove base64 image data from HTML content
    html_content = re.sub(r'data:image/png;base64,[^"]*', '', html_content)
    
    # Convert HTML content to markdown
    markdown_content = h.handle(html_content)
    return markdown_content


