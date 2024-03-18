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
    options.add_argument("--headless")
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
    print("Opening Browser ->>>>>>>")
    return driver

 
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
    options.add_argument("--headless")
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
    driver.get("https://www.linkedin.com")
    for cookie in cookies:
        driver.add_cookie(cookie)
    # driver.get("https://www.linkedin.com")
    driver.set_window_size(1920, 1080)
    print("Opening cookie Browser ->>>>>>>")
    return driver
async def openExistingUser(driver):
    print("Opening Existing Browser ->>>>>>>")
    driver.get("https://www.linkedin.com/feed")

# async def LinekdinLogin(email, password, driver):
#     driver.get("https://www.linkedin.com/login")
#     driver.find_element(By.XPATH, "*//input[@id = 'username']").send_keys(email)
#     time.sleep(await getrandomNumber(2,6))
#     driver.find_element(By.XPATH, "*//input[@id = 'password']").send_keys(password)
#     driver.find_element(By.XPATH, "*//button[@aria-label= 'Sign in']").click()
#     print("<<<<<<<- login into account succes   ->>>>>>>")
#     return True

async def LinekdinLogin(email, password, driver):
    driver.get("https://www.linkedin.com/login")
    driver.find_element(By.XPATH, "*//input[@id = 'username']").send_keys(email)
    time.sleep(await getrandomNumber(2,6))
    driver.find_element(By.XPATH, "*//input[@id = 'password']").send_keys(password)
    driver.find_element(By.XPATH, "*//button[@aria-label= 'Sign in']").click()
    textVerifycaptcha = "no"
    try:
        time.sleep(await getrandomNumber(8,12))
        isCaptch = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "*//h1")))
        if 'security' in isCaptch.text:
            textVerifycaptcha = "yes"
            print("<<<<<<<- capctha issue  ->>>>>>>")
            return False
    except:
        print("<<<<<<<- capctha issue  ->>>>>>>")
        return False
    print("<<<<<<<- login into account succes   ->>>>>>>")
    return True
    

async def startcampaign(campaigns, camapignData, driver, campaignid, fetchedresults):
    dataarray =[]
    searchurl = camapignData["searchItems"]
    if len(searchurl) == 0:
        return {"message": "No search Items"}
    steps = camapignData["steps"]
    # print(steps, ">>>>>>>>>")
    for url in searchurl:
        # print(url)
        like = False
        send_message_flag = False
        send_connection_request_flag = False
        send_inmail_flag = False
        link = url["query"]
        send_msg_content=""
        send_connection_msg=""
        send_inmail_msg=""
        resultNum = url["filter"]
        # print(link, resultNum)
        if 'sales' in url:
            for step in steps:
                send_inmail_flag = True
                inmail_subject = step["subject"]
                inmail_message = step["msg"]
            data = await search_sales(driver, link, resultNum, inmail_subject, inmail_message, campaigns, fetchedresults, campaignid)
            dataarray.extend(data)
        for step in steps:
            # print(step)
            if step["key"] == "like_3_posts":
                like = True
            if step["key"] == "send_message":
                send_message_flag = True
                send_msg_content = step["msg"]
            if step["key"] == "send_connection_request":
                send_connection_request_flag = True
                send_connection_msg = step["msg"]
        print("<<<<<<<- campaign started login into account succes   ->>>>>>>")
        print(">>>>>>>>>>>>>> " , like, send_message_flag, send_connection_request_flag, resultNum, "<<<<<<" )
        await getPageDataConnection(driver,link, resultNum,send_msg_content , send_connection_msg, like, send_message_flag, send_connection_request_flag, campaigns, fetchedresults, campaignid)
        # dataarray.extend(data)
    driver.quit()
    # return dataarray

async def getverificationCodeStatus(driver):
    codeFlag = False
    try :
        h1 = driver.find_element(By.XPATH, "*//h1[@class = 'content__header']").text
        if "verification" in h1:
            codeFlag = True        
    except Exception as e :
        print("<<<<<<<- exception    ->>>>>>>", e )
        codeFlag = False
    return codeFlag

from datetime import datetime
async def epoch_to_timestamp(epoch_time):
    try:
        timestamp = datetime.fromtimestamp(epoch_time)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
        # return timestamp.strptime(timestamp.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        return f"Error: {e}"
    
async def get_expiry_time(cookies):
    li_at_row = next(cookie for cookie in cookies if cookie['name'] == 'li_at')
    expiry = li_at_row.get('expiry', None)
    expiry = await epoch_to_timestamp(expiry)
    return expiry

async def verifyCode(code, driver):
    driver.find_element(By.XPATH, "*//input[@placeholder = 'Enter code']").send_keys(code)
    time.sleep(await getrandomNumber(2,5))
    driver.find_element(By.XPATH, "//button[normalize-space()='Submit']").click()
    return True
async def getCookies(driver):
    cookies = driver.get_cookies()
    return cookies

async def slow_type(element, text):
    delay = 60/300 # 5 characters per word
    for character in text:
        element.send_keys(character)
        time.sleep(delay)
        
async def send_message(result,message):
    WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Message']"))).click()
    time.sleep(await getrandomNumber(1, 3))
    element =  WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Write a message…']")))
    slow_type(element, message)
    WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Send']"))).click()
    WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Close your conversation with')]"))).click()

async def getPageDataConnection(driver, url, resultnum,send_msg_content , send_connection_msg, like , send_message_flag , send_connection_request_flag , campaigns, fetchedresults, campaignid):
    dataList = []
    driver.get(url)
    isDoneflag = False
    ConnectionSentCount = 0
    SendMessageCount =0
    LikeCount = 0
    # for i in range(1, int(resultnum)):
    i = 0
    while True:
        findResultList = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "*//li[@class='reusable-search__result-container']")))
        for result in findResultList:
            result_html = result.get_attribute('outerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')
            isconnected = "Not Connected"
            isMessage = "send Message not used"
            isLike = "not used"
            try:
                Name = soup.find('div', {'class': 't-roman t-sans'}).find('a').find('span').find('span').text.split(" ")
                firstname = Name[0]
                lastname = Name.pop()
                profileLink = soup.find('div', {'class': 't-roman t-sans'}).find('a')['href']
                profileImage = soup.find('div', {'class': 'presence-entity presence-entity--size-3'}).find('img')['src']
                UserTitle = soup.find('div', {'class': 'entity-result__primary-subtitle t-14 t-black t-normal'}).text.strip()
                adress = soup.find('div', {'class': 'entity-result__secondary-subtitle t-14 t-normal'}).text.strip()
                send_msg = send_msg_content.replace("{first_name}", firstname).replace("{last_name}", lastname)
               
                if send_message_flag:
                    try:
                        await send_message(result, send_msg)
                        SendMessageCount += 1
                        isMessage = "Message Sent!"
                    except:
                        isMessage = "Message Not Sent!"
                if like:
                    isLike = await likePost(driver, profileLink)
                    if isLike:
                        LikeCount +=1
                    time.sleep(await getrandomNumber(1, 3))
                if send_connection_request_flag:
                    send_updated_message = send_connection_msg.replace("{first_name}", firstname).replace("{last_name}", lastname)
                    try: 
                        WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Connect']"))).click()
                        time.sleep(await getrandomNumber(1, 3))
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a note']"))).click()
                        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//textarea[@id='custom-message']")))
                        await slow_type(element,send_updated_message)
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Send']"))).click()
                        isconnected = "Connection Request Sent!"
                        ConnectionSentCount += 1
                    except:
                        isconnected = await sendConnectionRequest(profileLink,send_updated_message, driver)
                        if isconnected == "Connection Request Sent!":
                            ConnectionSentCount += 1
                
                # company_name, profileLink = await getCompanyName(driver, profileLink)
                # dataDict = [{'FirstName': firstname, 'LastName': lastname , 'profileLink': profileLink,'profileimage' : profileImage , 'UserTitle': UserTitle, 'adress': adress , 'isconnected': isconnected['message'], 'isMessage': isMessage , 'isLike': isLike}]
                dataDict = {'FirstName': firstname, 'LastName': lastname , 'profileLink': profileLink,'profileimage' : profileImage , 'UserTitle': UserTitle,'address': adress , 'isconnected': isconnected, 'isMessage': isMessage , 'isLike': isLike}
                print(dataDict)
                if i ==0:
                    if fetchedresults.find_one({'campaign_id': campaignid}) == None:
                        result = {'campaign_id': campaignid, 'results': [dataDict]}
                        fetchedresults.insert_one(result)
                    else:
                        fetchedresults.update_one({'campaign_id': campaignid}, {'$push': {'results': dataDict}})
                else:
                    fetchedresults.update_one({'campaign_id': campaignid}, {'$push': {'results': dataDict}})
                # campaigns.update_one({'campaign_id': campaignid}, {'$set': {'status': 'running'}})
                campaigns.update_one({'campaign_id': campaignid}, {'$set': {'progress': i+1,'connected_people': ConnectionSentCount, 'message_send': SendMessageCount, 'liked': LikeCount}})
                time.sleep(await getrandomNumber(1, 3))
                if i == int(resultnum):
                    print("<<<<<< done success campagin >>>>>>> ")
                    isDoneflag = True
                    break
                i += 1
                # dataList.append({'FirstName': firstname, 'LastName': lastname , 'profileLink': profileLink,'profileimage' : profileImage , 'UserTitle': UserTitle, 'adress': adress , 'isconnected': isconnected, 'isMessage': isMessage , 'isLike': isLike})
                    # dataList.append({'Name': Name, 'profileLink': profileLink, 'UserTitle': UserTitle, 'adress': adress , 'message': message })
            except Exception as e:
                print("<<<<<< error in result gathering data >>>>>>> ", e)
                continue
            
        if isDoneflag:
            campaigns.update_one({'campaign_id': campaignid}, {'$set': {'status': 'completed'}})
            break
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[@aria-label='Next']"))).click()
        
    # return dataList
async def getCompanyName(driver, url):
    original_window = driver.window_handles[0]
    driver.switch_to.new_window('tab')
    company_name = "Not Found"
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='ph5 pb5']//ul[@class = 'pv-text-details__right-panel']/li)[1]"))).text
    except  Exception as e:
        company_name = "Not Found"
        print("<<<<<< error in getting company name >>>>>>> ", e)
    linkedinUrl = driver.current_url
    print("<<<<<< getting company name >>>>>>> ", company_name)
    driver.close()
    driver.switch_to.window(original_window)
    return company_name.text, linkedinUrl

async def sendInMail(driver, subject, message):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Subject (required)']"))).send_keys(subject)
    time.sleep(await getrandomNumber(2, 5))
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Type your message here…']")))
    await slow_type(element, message)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Send']"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-control-name='overlay.close_overlay']"))).click()
    print("<<<<<< inmail sent success >>>>>>> ")
    return True

async def search_sales(driver,url, result_num, subject, message, campaigns, fetchedresults, campaignid):
    driver.get(url)
    DataList = []
    i = 0
    immail_sent = 0
    loopflag = False
    while True:
        findResultList = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "*//li[@class='artdeco-list__item pl3 pv3 ']")))
        for result in findResultList:
            driver.execute_script("arguments[0].scrollIntoView();", result)
            result_html = result.get_attribute('outerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')
            try:
                name = soup.find('span', {'data-anonymize': 'person-name'}).text.strip().split()
                address = soup.find('span', {'data-anonymize': 'location'}).text.strip()
                profile_image = soup.find('img', {"data-anonymize":"headshot-photo"}).get('src')
                firstname = name[0]
                lastname = name.pop()
                link_tag = soup.find('a', {'data-view-name': 'search-results-lead-name'})
                link ="https://www.linkedin.com"+link_tag.get('href')
                data = {
                    'firstname': firstname,
                    'lastname': lastname,
                    'address': address,
                    'profile_image' : profile_image,
                    'profile_link': link,
                    'type': 'salesnavigator'
                }
                WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, ".//li[@class='message-overlay-trigger']"))).click()
                try:
                    message = message.replace("{first_name}", firstname).replace("{last_name}", lastname)
                    is_inmail = await sendInMail(driver, subject, message)
                except:
                    is_inmail = False
                data['inmail'] = is_inmail
                if is_inmail:
                    print("<<<<<< inmail sent success >>>>>>> ")
                    immail_sent += 1
                if i == 0:
                    if fetchedresults.find_one({'campaign_id': campaignid}) == None:
                        result = {'campaign_id': campaignid,'type': 'salesnavigator' ,'results': [data] }
                        fetchedresults.insert_one(result)
                    
                    result = {'campaign_id': campaignid,'type': 'salesnavigator' ,'results': data }
                    fetchedresults.update_one(result)
                else:
                    fetchedresults.update_one({'campaign_id': campaignid}, {'$push': {'results': data}})
                # campaigns.update_one({'campaign_id': campaignid}, {'$set': {'status': 'running'}})
                campaigns.update_one({'campaign_id': campaignid}, {'$set': {'progress': i, 'connected_people': 'notused', 'message_send': 'notused', 'liked': 'notused', 'inmail_sent': immail_sent}})
                # DataList.append(data)
                if i >= result_num:
                    loopflag = True
                    break    
                i += 1
            except :
                continue
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Next']"))).click()
            
        if loopflag:
            break
    driver.quit()
    # return DataList
    # print(soup.prettify())


async def likePost(driver, profile_url):
    original_window = driver.window_handles[0]
    driver.switch_to.new_window('tab')
    driver.get(profile_url)
    profile_url = driver.current_url
    driver.get(profile_url+"recent-activity/all/")
    isLiked = False
    i=0
    try:
        # print("Likepost => ", profile_url)
        allPost = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "*//li[@class='profile-creator-shared-feed-update__container']")))
        for post in allPost:
            driver.execute_script("arguments[0].scrollIntoView();", post)
            WebDriverWait(post, 10).until(EC.presence_of_element_located((By.XPATH, ".//button[normalize-space()='Like']"))).click()
            time.sleep(await getrandomNumber(2, 5))
            i+=1
            if i > 3:
                print("<<<<<< like post success >>>>>>> ")
                isLiked = True
                break
    except:
        pass
    driver.close()
    driver.switch_to.window(original_window)
    return isLiked
        

# async def getNextPage(driver):
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[@aria-label='Next']"))).click()
# async def sendRequest(dataList, driver):
#     for data in dataList:
#         isconnect = await sendConnectionRequest(data['profileLink'], data['message'], driver)
#         data['isconnected'] = isconnect
#     return dataList
async def sendConnectionRequest(link, message, driver):
    original_window = driver.window_handles[0]
    driver.switch_to.new_window('tab')
    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//div[@class='ph5 pb5']//button[normalize-space()='Connect']"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a note']"))).click()
        time.sleep(await getrandomNumber(1,3))
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//textarea[@id='custom-message']")))
        await slow_type(element, message)
        time.sleep(await getrandomNumber(3,6))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Send']"))).click()
        driver.close()
        driver.switch_to.window(original_window)
        print("<<<<<<<<<< 1st try Connection Request Sent! >>>>>>>>>")
        return "Connection Request Sent!"
    except:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(*//button[normalize-space()='More'])[2]"))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[starts-with(@aria-label, 'Invite')])[2]"))).click()
            time.sleep(await getrandomNumber(1,3))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Add a note']"))).click()
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//textarea[@id='custom-message']")))
            await slow_type(element, message)
            time.sleep(await getrandomNumber(3,4))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "*//button[normalize-space()='Send']"))).click()
            driver.close()
            driver.switch_to.window(original_window)
            print("<<<<<<<<<< second try  Connection Request Sent! >>>>>>>>>")
            return "Connection Request Sent!"
        except :
            driver.close()
            driver.switch_to.window(original_window)
            return "existing connection!"