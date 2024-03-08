from fastapi import Depends, FastAPI, Query, HTTPException
from typing import List, Dict, Any
from fastapi.responses import HTMLResponse  
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from linkedin import openBrowser, openBrowserUserCookies, LinekdinLogin, getverificationCodeStatus, verifyCode, getCookies, doSearch, getTotalPage, getPageDataConnection, sendConnectionRequest, getNextPage
app = FastAPI()

origins = [
    "https://backend.sddoc.in",
    "https://backend.sddoc.in/",
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

# Store a mapping of user sessions to drivers
user_sessions: Dict[str, Any] = {}

async def get_driver(user_session: str = Query(...)):
    driver = await openBrowser()
    return driver

async def get_authenticated_driver(cookies: str = Query(...)):
    driver = await openBrowserUserCookies(eval(cookies))
    return driver

@app.get("/openexisting")
async def openexisting(cookies: str = Query(...), driver=Depends(get_authenticated_driver)):
    return JSONResponse(content={"message": "Browser Opened!"})


@app.get("/login")
async def login(email: str = Query(...), password: str = Query(...), driver = Depends(get_driver)):
    await LinekdinLogin(email, password, driver)
    return JSONResponse(content={"message": "Login Successful!"})

@app.get("/getcodestatus")
async def getCodeStatus(driver = Depends(get_driver)):
    codeFlag = await getverificationCodeStatus(driver)
    return JSONResponse(content={"codeFlag": codeFlag})

@app.get("/verifyCode")
async def verifcode(code: str = Query(...), driver = Depends(get_driver)):
    codestatuse = await verifyCode(code)
    if codestatuse:
        cookies = await getCookies(driver)
        return JSONResponse(content={"message": "Code Verified!", "cookies": cookies})
    else:
        return JSONResponse(content={"message": "Code Not Verified!"})

@app.get("/search")
async def search(serachname: str = Query(...), titlekeyword: str = Query(...), location: str = Query(...), connectiontype: List[str] = Query(...), company: str = Query(...), driver = Depends(get_driver)):
    await doSearch(serachname, titlekeyword, location, connectiontype, company,driver)
    return JSONResponse(content={"message": "Search Successful!"})

@app.get("/totalpage")
async def totalPage(driver = Depends(get_driver)):
    totalPage = await getTotalPage(driver)
    return JSONResponse(content={"totalPage": totalPage})
@app.get("/getpage")
async def pageDataConnection(driver = Depends(get_driver)):
    data = await getPageDataConnection(driver)
    return JSONResponse(content=data)


@app.get("/connect")
async def sendConnection(driver = Depends(get_driver)):
    await sendConnectionRequest()
    return JSONResponse(content={"message": "Connection Request Sent!"})


@app.get("/")
async def read_root():
    return JSONResponse(content={"message": "Welcome to this app!"})
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80)