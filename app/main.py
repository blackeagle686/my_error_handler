
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import router
from app.core.config import settings
import os

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Mount Static Files
static_dir = os.path.join(os.getcwd(), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/css", StaticFiles(directory=os.path.join(static_dir, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(static_dir, "js")), name="js")

# API Routes
app.include_router(router, prefix="/api")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
