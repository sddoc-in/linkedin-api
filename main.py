from fastapi import Depends, FastAPI, Query, HTTPException
from typing import List, Dict, Any
import uuid
from fastapi.responses import HTMLResponse  
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from linkedin import openBrowser, openBrowserUserCookies, LinekdinLogin, getverificationCodeStatus, verifyCode, getCookies, doSearch, getTotalPage, getPageDataConnection, sendConnectionRequest, getNextPage
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

async def get_driver(session_id: str =Query(default_factory=lambda: str(uuid.uuid4()))):
    if session_id not in driver_pool:
        driver_pool[session_id] = await openBrowser()  

    # Return the existing or newly created driver for the session ID
    return driver_pool[session_id] , session_id


async def get_session_driver(session_id: str = Query(...)):
    if session_id not in driver_pool:
        driver_pool[session_id] = await openBrowser()
    return driver_pool[session_id]

async def get_authenticated_driver(cookies: str = Query(...), session_id: str =Query(default_factory=lambda: str(uuid.uuid4()))):
    if session_id not in driver_pool:
        # If the session ID is not in the pool, create a new driver
        driver_pool[session_id] = await openBrowserUserCookies(cookies)  # Use Chrome
    return driver_pool[session_id], session_id

# @app.get("/openexisting")
# async def openexisting(cookies: str = Query(...), driver=Depends(get_authenticated_driver)):
#     return JSONResponse(content={"message": "Browser Opened!"})


@app.get("/login")
async def login(email: str = Query(...), password: str = Query(...), driver_session: tuple =Depends(get_driver)):
    driver, session_id = driver_session
    await LinekdinLogin(email, password, driver)
    return JSONResponse(content={"message": "Login Successful!", "session":session_id})

@app.get("/getcodestatus")
async def getCodeStatus(session_id: str = Query(...), driver = Depends(get_session_driver)):
    codeFlag = await getverificationCodeStatus(driver)
    return JSONResponse(content={"codeFlag": codeFlag , "session":session_id})

@app.get("/verifyCode")
async def verifcode(code: str = Query(...), session_id: str = Query(...), driver = Depends(get_session_driver)):
    codestatuse = await verifyCode(code, driver)
    if codestatuse:
        cookies = await getCookies(driver)
        return JSONResponse(content={"message": "Code Verified!", "cookies": cookies , "session":session_id})
    else:
        return JSONResponse(content={"message": "Code Not Verified!"})

@app.get("/search")
async def search(serachname: str = Query(...), titlekeyword: str = Query(...), location: str = Query(...), connectiontype: List[str] = Query(...), company: str = Query(...), session_id: str = Query(...),driver = Depends(get_session_driver)):
    isSuccess = await doSearch(serachname, titlekeyword, location, connectiontype, company,driver)
    if isSuccess:
        return JSONResponse(content={"message": "Search Successful!"})
    else:
        return JSONResponse(content={"message": "Search Unsuccessful retry again!"})

@app.get("/totalpage")
async def totalPage(session_id: str = Query(...), driver = Depends(get_session_driver)):
    totalPage = await getTotalPage(driver)
    return JSONResponse(content={"totalPage": totalPage})
@app.get("/getpage")
async def pageDataConnection(session_id: str = Query(...), driver = Depends(get_session_driver)):
    data = await getPageDataConnection(driver)
    return JSONResponse(content=data)

@app.get("/nextpage")
async def nextpage(session_id: str = Query(...), driver = Depends(get_session_driver)):
    await getNextPage(driver)
    return JSONResponse(content={"message": "Next Page Clicked!"})

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