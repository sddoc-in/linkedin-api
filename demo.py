from fastapi import Depends, FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dictionary to store Selenium drivers and associate them with session IDs
driver_pool = {}

# Dependency to get or create a Selenium driver based on a session ID
async def get_driver(session_id: str = Query(...)):
    if session_id not in driver_pool:
        # If the session ID is not in the pool, create a new driver
        driver_pool[session_id] = webdriver.Chrome()  # Use Chrome as an example

    # Return the existing or newly created driver for the session ID
    return driver_pool[session_id]

@app.get("/open-google")
async def open_google(session_id: str = Query(...), driver=Depends(get_driver)):
    try:
        # Open Google using the existing or newly created driver
        driver.get("https://www.google.com")
        return JSONResponse(content={"message": f"Google opened for session ID: {session_id}"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

@app.get("/search")
async def search_google(query: str = Query(...), session_id: str = Query(...), driver=Depends(get_driver)):
    try:
        # Perform a search on Google using the existing or newly created driver
        search_box = driver.find_element("name", "q")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        return JSONResponse(content={"message": f"Search performed for session ID: {session_id}"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
