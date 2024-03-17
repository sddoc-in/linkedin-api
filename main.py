from fastapi import Depends, FastAPI, Query, HTTPException, Body
from typing import List, Dict, Any
import uuid
from urllib.parse import unquote
import logging 
from fastapi.responses import HTMLResponse  
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from bson import ObjectId
from linkedin import openBrowser, openBrowserUserCookies, LinekdinLogin, getverificationCodeStatus, verifyCode, getCookies, get_expiry_time, sendConnectionRequest, openExistingUser , startcampaign

uri = "mongodb+srv://admin:BTzG4AjRskOaeFeb@leads.nhrq5wp.mongodb.net?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.client
campaigns = db.campaigns
fetchedresults = db['fetched-results']
app = FastAPI()

origins = [
    "https://leads.sddoc.in",
    "https://leads.sddoc.in/",
    "http://localhost:3000",
    "http://localhost:3000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

driver_pool = {}


proxies = [
    ("38.154.227.167", 5868, "tszuwnnm", "g0q5bywh7j1l"),
    ("185.199.229.156", 7492, "tszuwnnm", "g0q5bywh7j1l"),
    ("185.199.228.220", 7300, "tszuwnnm", "g0q5bywh7j1l"),
    ("185.199.231.45", 8382, "tszuwnnm", "g0q5bywh7j1l"),
    ("188.74.210.207", 6286, "tszuwnnm", "g0q5bywh7j1l"),
    ("188.74.183.10", 8279, "tszuwnnm", "g0q5bywh7j1l"),
    ("188.74.210.21", 6100, "tszuwnnm", "g0q5bywh7j1l"),
    ("45.155.68.129", 8133, "tszuwnnm", "g0q5bywh7j1l"),
    ("154.95.36.199", 6893, "tszuwnnm", "g0q5bywh7j1l"),
    ("45.94.47.66", 8110, "tszuwnnm", "g0q5bywh7j1l")
]

# async def get_driver(session_id: str =Query(default_factory=lambda: str(uuid.uuid4()))):
#     if session_id not in driver_pool:
#         driver_pool[session_id] = await openBrowser()  

#     # Return the existing or newly created driver for the session ID
#     return driver_pool[session_id] , session_id

async def get_driver(proxy_address: str = Query(...),
    proxy_port: str = Query(...),
    proxy_username: str = Query(...),
    proxy_password: str = Query(...), session_id: str =Query(default_factory=lambda: str(uuid.uuid4()))):
    # print(proxy_address, proxy_port, proxy_username, proxy_password , "hey")
    if session_id not in driver_pool:
        driver_pool[session_id] = await openBrowser(proxy_address, proxy_port, proxy_username, proxy_password)  

    # Return the existing or newly created driver for the session ID
    return driver_pool[session_id] , session_id


async def get_session_driver(session_id: str = Query(...)):
    if session_id not in driver_pool:
        # driver_pool[session_id] = await openBrowser()
        pass
    return driver_pool[session_id]

async def get_authenticated_driver(proxy_address: str = Query(...),
    proxy_port: str = Query(...),
    proxy_username: str = Query(...),
    proxy_password: str = Query(...),cookiedata: dict= Body(...), session_id: str =Query(default_factory=lambda: str(uuid.uuid4()))):
    proxy_username = unquote(proxy_username)
    proxy_password = unquote(proxy_password)
    if session_id not in driver_pool:
        # If the session ID is not in the pool, create a new driver
        driver_pool[session_id] = await openBrowserUserCookies(cookiedata['cookies'], proxy_address, proxy_port, proxy_username, proxy_password )  # Use Chrome
    return driver_pool[session_id], session_id

@app.post("/openexisting")
async def openexisting(driver_session: tuple =Depends(get_authenticated_driver)):
    driver, session_id = driver_session
    try:
        await openExistingUser(driver)
    except Exception as e:
        return JSONResponse(content={"message": "Cookie Error in opening existing user!", "error": str(e)})
    return JSONResponse(content={"session": session_id })


@app.get("/login")
async def login(email: str = Query(...), password: str = Query(...), driver_session: tuple =Depends(get_driver)):
    driver, session_id = driver_session
    email = unquote(email)
    password = unquote(password)
    await LinekdinLogin(email, password, driver)
    cookies = await getCookies(driver)
    codeFlag = await getverificationCodeStatus(driver)
    message = "Login Successful!"
    if codeFlag:
        message = "Verification Code Required!"
        return JSONResponse(content={"message": message, "session":session_id, "cookies": "not found", 'codeFlag': codeFlag})
    closeUserBrowser(session_id, driver)
    # expiry_time = await get_expiry_time(cookies)
    await closeBrowser(session_id, driver)
    return JSONResponse(content={"message": message, "session":session_id, "cookies": cookies,'codeFlag': codeFlag})

@app.get("/getcodestatus")
async def getCodeStatus(session_id: str = Query(...), driver = Depends(get_session_driver)):
    codeFlag = await getverificationCodeStatus(driver)
    return JSONResponse(content={"codeFlag": codeFlag , "session":session_id})

@app.get("/verifyCode")
async def verifcode(code: str = Query(...), session_id: str = Query(...), driver = Depends(get_session_driver)):
    codestatuse = await verifyCode(code, driver)
    if codestatuse:
        cookies = await getCookies(driver)
        expiry_time = await get_expiry_time(cookies)
        closeUserBrowser(session_id, driver)
        return JSONResponse(content={"message": "Code Verified!", "cookies": cookies , "session":session_id, "expire": expiry_time})
    else:
        return JSONResponse(content={"message": "Code Not Verified!"})

# @app.get("/search")
# async def search(serachname: str = Query(...), titlekeyword: str = Query(...), location: str = Query(...), connectiontype: List[str] = Query(...), company: str = Query(...), session_id: str = Query(...),driver = Depends(get_session_driver)):
#     isSuccess = await doSearch(serachname, titlekeyword, location, connectiontype, company,driver)
#     if isSuccess:
#         return JSONResponse(content={"message": "Search Successful!"})
#     else:
#         return JSONResponse(content={"message": "Search Unsuccessful retry again!"})

# @app.get("/totalpage")
# async def totalPage(session_id: str = Query(...), driver = Depends(get_session_driver)):
#     totalPage = await getTotalPage(driver)
#     return JSONResponse(content={"totalPage": totalPage})

@app.get("/start")
async def search(campaignid :str = Query(...),session_id: str = Query(...) ,driver = Depends(get_session_driver)):
    campaign = campaigns.find_one({"campaign_id": campaignid})
    startcampaign(campaigns, campaign, driver, campaignid, fetchedresults)
    return JSONResponse(content={"message": "Campaign Started!", "session":session_id})

# @app.get("/nextpage")
# async def nextpage(session_id: str = Query(...), driver = Depends(get_session_driver)):
#     await getNextPage(driver)
#     return JSONResponse(content={"message": "Next Page Clicked!"})

def closeUserBrowser(session_id, driver):
    driver.quit()
    del driver_pool[session_id]
    return JSONResponse(content={"message": "Browser Closed!"})


@app.get("/close")
async def closeBrowser(session_id: str = Query(...), driver = Depends(get_session_driver)):
    driver.quit()
    del driver_pool[session_id]
    return JSONResponse(content={"message": "Browser Closed!"})

@app.get("/connect")
async def sendConnection(url : str = Query(...), message : str = Query(...) ,session_id: str = Query(...), driver = Depends(get_session_driver)):
    await sendConnectionRequest(url, message, driver)
    return JSONResponse(content={"message": "Connection Request Sent!"})


@app.get("/")
async def read_root():
    return JSONResponse(content={"message": "Welcome to this app!"})
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)
