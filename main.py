from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_browser():
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.linkedin.com/in/darakhsha-rayen-a81a33222/")
        return driver
    except Exception as e:
        print("Error:", e)
        return None

def scrape_profile_info(driver):
    try:
        profile_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='HrNUTdMgZdKRzKknXaeWVHpYukeRpcBoM']")))
        print("Profile Name:", profile_name.text)
        
        profile = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//div[@data-generated-suggestion-target='urn:li:fsu_profileActionDelegate:-579158814']")))
        print("Profile:", profile.text)
        
        address = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//span[@class='text-body-small inline t-black--light break-words']")))
        print("Address:", address.text)
        
        email_address = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//a[@id='top-card-text-details-contact-info']"))).click()
        email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//div[@class='pv-contact-info__ci-container t-14'])[2]")))
        print("Email:", email.text)
        
        company_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//span[@class='t-14 t-normal'])[6]")))
        print("Company Name:", company_name.text)
        full_text = company_name.text
        desired_text = full_text.split("·")[0].strip()
        print("Desired Company Name:", desired_text)
        
        profile_photo_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='profile-photo-edit__edit-btn']")))
        img_element = profile_photo_button.find_element(By.XPATH, "./img")
        image_url = img_element.get_attribute("src")
        print("Image URL:", image_url)
    except Exception as e:
        print("Error:", e)

# Open browser and scrape profile info
browser_driver = open_browser()
if browser_driver:
    scrape_profile_info(browser_driver)
    browser_driver.quit()
