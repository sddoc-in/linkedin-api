from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time    
from bs4 import BeautifulSoup
async def openBrowser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    # Set user agent to simulate a specific browser
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

    # Enable automation features to make the browser look more like a real user
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    # driver.maximize_window()
    return driver
    
def openBrowserUserCookies(cookies):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    driver = webdriver.Chrome(options=options)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.set_window_size(1920, 1080)
    driver.get("https://www.linkedin.com")
    return driver
    
async def LinekdinLogin(email, password, driver):
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.XPATH, "*//input[@id = 'username']").send_keys(email)
    driver.find_element(By.XPATH, "*//input[@id = 'password']").send_keys(password)
    driver.find_element(By.XPATH, "*//button[@aria-label= 'Sign in']").click()
    
    return True
    

async def getverificationCodeStatus(driver):
    codeFlag = False
    try :
        h1 = driver.find_element(By.XPATH, "*//h1[@class = 'content__header']").text
        if "verification" in h1:
            codeFlag = True        
    except:
        codeFlag = False
    return codeFlag


async def verifyCode(code, driver):
    driver.find_element(By.XPATH, "*//input[@placeholder = 'Enter code']").send_keys(code)
    driver.find_element(By.XPATH, "//button[normalize-space()='Submit']").click()
    return True
async def getCookies(driver):
    cookies = driver.get_cookies()
    return cookies


async def doSearch(serachName, titleKeyword, location, connectionType, company, driver):
    driver.get("https://www.linkedin.com/feed/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder='Search']"))).send_keys(serachName)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder='Search']"))).send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//button[normalize-space()='People'])[1]"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='All filters']"))).click()
    # driver.find_element(By.XPATH, "*//button[normalize-space()='All filters']").click()
    if connectionType:
        for i in connectionType:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"*//label[@for = 'advanced-filter-network-{i}']"))).click()
            # driver.find_element(By.XPATH, f"*//label[@for = 'advanced-filter-network-{i}']").click()
    
    if location:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a location']"))).click()
        # driver.find_element(By.XPATH, "*//button[normalize-space()='Add a location']").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder = 'Add a location']"))).send_keys(location)
        # driver.find_element(By.XPATH, "*//input[@placeholder = 'Add a location']").send_keys(location)
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder = 'Add a location']"))).send_keys(Keys.ARROW_DOWN)
        # driver.find_element(By.XPATH, "*//input[@placeholder = 'Add a location']").send_keys(Keys.ARROW_DOWN)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder = 'Add a location']"))).send_keys(Keys.ENTER)
        # driver.find_element(By.XPATH, "*//input[@placeholder = 'Add a location']").send_keys(Keys.ENTER)
    if titleKeyword:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//label[normalize-space()= 'Title']/input"))).send_keys(titleKeyword)
        # driver.find_element(By.XPATH, "*//label[normalize-space()= 'Title']/input").send_keys(titleKeyword)
    if company:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//label[normalize-space()= 'Company']/input"))).send_keys(company)
        # driver.find_element(By.XPATH, "*//label[normalize-space()= 'Company']/input").send_keys(company)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//button[normalize-space()='Show results'])[1]"))).click()
    # driver.find_element(By.XPATH, "(*//button[normalize-space()='Show results'])[1]").click()


async def getTotalPage(driver):
    totalPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//div[@class = 'artdeco-pagination__page-state']"))).text
    return int(totalPage.split('of')[1].strip())

# async def getPageDataConnection(driver):
#     dataList = []
#     findResultList = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "*//li[@class='reusable-search__result-container']")))
#     for result in findResultList:
#         # Name =  result.find_element(By.XPATH, ".//div[@class='t-roman t-sans']//div/span/span/a/span/span").text.strip()
#         Name =  WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='t-roman t-sans']//div/span/span/a/span/span"))).text
#         # profileLink = result.find_element(By.XPATH, ".//div[@class='t-roman t-sans']/div/span/span/a").get_attribute('href')
#         profileLink  =  WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='t-roman t-sans']//div/span/span/a"))).get_attribute('href')
#         # UserTitle = result.find_element(By.XPATH, ".//div[@class='entity-result__primary-subtitle t-14 t-black t-normal']").text.strip()
#         UserTitle = WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='entity-result__primary-subtitle t-14 t-black t-normal']"))).text
#         # address = result.find_element(By.XPATH, ".//div[@class='entity-result__secondary-subtitle t-14 t-normal']").text.strip()
#         address = WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='entity-result__secondary-subtitle t-14 t-normal']"))).text
#         dataList.append({'Name': Name, 'profileLink': profileLink, 'UserTitle': UserTitle, 'adress': address})
#     return dataList

async def getPageDataConnection(driver):
    dataList = []
    findResultList = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "*//li[@class='reusable-search__result-container']")))
    for result in findResultList:
        result_html = result.get_attribute('outerHTML')
        soup = BeautifulSoup(result_html, 'html.parser')
       
        try:
            Name = soup.find('div', {'class': 't-roman t-sans'}).find('a').find('span').find('span').text
            profileLink = soup.find('div', {'class': 't-roman t-sans'}).find('a')['href']
            UserTitle = soup.find('div', {'class': 'entity-result__primary-subtitle t-14 t-black t-normal'}).text.strip()
            adress = soup.find('div', {'class': 'entity-result__secondary-subtitle t-14 t-normal'}).text.strip()
            dataList.append({'Name': Name, 'profileLink': profileLink, 'UserTitle': UserTitle, 'adress': adress})
        except:
            continue
    return dataList

async def getNextPage(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[@aria-label='Next']"))).click()


async def sendConnectionRequest(link, message, driver):
    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//div[@class='ph5 pb5']//button[normalize-space()='Connect']"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a note']"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//textarea[@id='custom-message']"))).send_keys(message)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Send']"))).click()
    except:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//button[normalize-space()='More'])[2]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[starts-with(@aria-label, 'Invite')])[2]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a note']"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//textarea[@id='custom-message']"))).send_keys(message)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Send']"))).click()
            