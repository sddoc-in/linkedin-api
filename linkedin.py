from seleniumwire import webdriver
# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time , random    
from bs4 import BeautifulSoup


async def openBrowser(proxy_address, proxy_port, proxy_username, proxy_password ):
    options = Options()
    proxy = {
        'proxy': {
            'https': f'https://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}',
        }
    }
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    # options.add_argument("--headless")
    # options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    # Enable automation features to make the browser look more like a real user
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    if proxy_address == "not":
        driver = webdriver.Chrome(options=options)
        # driver.get('https://www.whatismypublicip.com/')
        driver.set_window_size(1920, 1080)
    else:
        driver = webdriver.Chrome(seleniumwire_options=proxy,options=options)
        # driver.get('https://www.whatismypublicip.com/')
        driver.set_window_size(1920, 1080)
    return driver


# async def openBrowser():
#     options = Options()
    
#     # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     # options.add_argument("--headless")
#     # options.add_argument(f'user-agent={user_agent}')
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-extensions")
#     options.add_argument("--disable-software-rasterizer")
#     # Enable automation features to make the browser look more like a real user
#     options.add_experimental_option('excludeSwitches', ['enable-automation'])
#     options.add_experimental_option('useAutomationExtension', False)
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     driver = webdriver.Chrome(options=options)
#     driver.set_window_size(1920, 1080)
#     return driver
 
async def getrandomNumber(min, max):
    return random.randint(min, max)
    
async def openBrowserUserCookies(cookies, proxy_address, proxy_port, proxy_username, proxy_password):
    options = Options()
    proxy = {
        'proxy': {
            'https': f'https://{proxy_username}:{proxy_password}@{proxy_address}:{proxy_port}',
        }
    }
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    # options.add_argument("--headless")
    # options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    # Enable automation features to make the browser look more like a real user
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(seleniumwire_options=proxy,options=options)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.set_window_size(1920, 1080)
    
    return driver
async def openExistingUser(driver):
    driver.get("https://www.linkedin.com")

async def LinekdinLogin(email, password, driver):
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.XPATH, "*//input[@id = 'username']").send_keys(email)
    time.sleep(await getrandomNumber(2,6))
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
    time.sleep(await getrandomNumber(2,5))
    driver.find_element(By.XPATH, "//button[normalize-space()='Submit']").click()
    return True
async def getCookies(driver):
    cookies = driver.get_cookies()
    return cookies


# async def doSearch(serachName, titleKeyword, location, connectionType, company, driver):
#     try:
#         driver.get("https://www.linkedin.com/feed/")
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder='Search']"))).send_keys(serachName)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder='Search']"))).send_keys(Keys.ENTER)
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//button[normalize-space()='People'])[1]"))).click()
#         time.sleep(await getrandomNumber(1,3))
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='All filters']"))).click()
#         # driver.find_element(By.XPATH, "*//button[normalize-space()='All filters']").click()
#         time.sleep(await getrandomNumber(1,3))
#         if connectionType:
#             for i in connectionType:
#                 WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"*//label[@for = 'advanced-filter-network-{i}']"))).click()
#                 time.sleep(await getrandomNumber(1,3))
#                 # driver.find_element(By.XPATH, f"*//label[@for = 'advanced-filter-network-{i}']").click()
        
#         if location:
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a location']"))).click()
#             # driver.find_element(By.XPATH, "*//button[normalize-space()='Add a location']").click()
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder = 'Add a location']"))).send_keys(location)
#             # driver.find_element(By.XPATH, "*//input[@placeholder = 'Add a location']").send_keys(location)
#             time.sleep(await getrandomNumber(2,3))
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder = 'Add a location']"))).send_keys(Keys.ARROW_DOWN)
#             # driver.find_element(By.XPATH, "*//input[@placeholder = 'Add a location']").send_keys(Keys.ARROW_DOWN)
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//input[@placeholder = 'Add a location']"))).send_keys(Keys.ENTER)
#             # driver.find_element(By.XPATH, "*//input[@placeholder = 'Add a location']").send_keys(Keys.ENTER)
#         if titleKeyword:
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//label[normalize-space()= 'Title']/input"))).send_keys(titleKeyword)
#             # driver.find_element(By.XPATH, "*//label[normalize-space()= 'Title']/input").send_keys(titleKeyword)
#             time.sleep(await getrandomNumber(1,3))
#         if company:
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//label[normalize-space()= 'Company']/input"))).send_keys(company)
#             # driver.find_element(By.XPATH, "*//label[normalize-space()= 'Company']/input").send_keys(company)
#             time.sleep(await getrandomNumber(1,3))
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//button[normalize-space()='Show results'])[1]"))).click()
#         return True
#     # driver.find_element(By.XPATH, "(*//button[normalize-space()='Show results'])[1]").click()
#     except :
#         return False


async def getTotalPage(driver):
    totalPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'results')]"))).text
    return totalPage

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

async def getPageDataConnection(driver, url, resultnum, message):
    dataList = []
    driver.get(url)
    for i in range(1, int(resultnum)):
        findResultList = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "*//li[@class='reusable-search__result-container']")))
        for result in findResultList:
            result_html = result.get_attribute('outerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')
        
            try:
                Name = soup.find('div', {'class': 't-roman t-sans'}).find('a').find('span').find('span').text
                profileLink = soup.find('div', {'class': 't-roman t-sans'}).find('a')['href']
                UserTitle = soup.find('div', {'class': 'entity-result__primary-subtitle t-14 t-black t-normal'}).text.strip()
                adress = soup.find('div', {'class': 'entity-result__secondary-subtitle t-14 t-normal'}).text.strip()
                message= message.replace("{{name}}", Name)
                # isconnected = await sendConnectionRequest(profileLink, message, driver)
                # dataList.append({'Name': Name, 'profileLink': profileLink, 'UserTitle': UserTitle, 'adress': adress , 'isconnected': isconnected})
                dataList.append({'Name': Name, 'profileLink': profileLink, 'UserTitle': UserTitle, 'adress': adress })
            except:
                continue
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[@aria-label='Next']"))).click()
    dataList = await sendRequest(dataList, driver)
    return dataList

# async def getNextPage(driver):
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[@aria-label='Next']"))).click()
async def sendRequest(dataList, driver):
    for data in dataList:
        isconnect = await sendConnectionRequest(data['profileLink'], data['message'], driver)
        data['isconnected'] = isconnect
    return dataList
async def sendConnectionRequest(link, message, driver):
    original_window = driver.window_handles[0]
    driver.switch_to.new_window('tab')
    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//div[@class='ph5 pb5']//button[normalize-space()='Connect']"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a note']"))).click()
        time.sleep(await getrandomNumber(1,3))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//textarea[@id='custom-message']"))).send_keys(message)
        time.sleep(await getrandomNumber(2,6))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Send']"))).click()
        driver.close()
        driver.switch_to.window(original_window)
        return {"message": "Connection Request Sent!"}
    except:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//button[normalize-space()='More'])[2]"))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[starts-with(@aria-label, 'Invite')])[2]"))).click()
            time.sleep(await getrandomNumber(1,3))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a note']"))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//textarea[@id='custom-message']"))).send_keys(message)
            time.sleep(await getrandomNumber(2,6))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Send']"))).click()
            driver.close()
            driver.switch_to.window(original_window)
            return {"message": "Connection Request Sent!"}
        except :
            driver.close()
            driver.switch_to.window(original_window)
            return {"message": "existing connection!"}