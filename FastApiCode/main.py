from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers.authentication import router as auth_router
from routers.routers import router as general_router

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("pages/Homepage.html")

app.include_router(auth_router)
app.include_router(general_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)