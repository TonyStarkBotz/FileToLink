from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database.connection import settings, files_col, create_indexes
from app.streamer.manager import session_manager
from app.streamer.engine import get_streaming_response
from app.bot.main import register_handlers
from app.admin.routes import router as admin_router
import uvicorn
import asyncio
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Telegram Direct Media Link Generator")

# Include Routers
app.include_router(admin_router)

# Mount Static Files & Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    await create_indexes()
    await session_manager.start()
    register_handlers(session_manager.bot_client)
    logger.info("Application started")

@app.on_event("shutdown")
async def shutdown_event():
    await session_manager.stop()
    logger.info("Application stopped")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/watch/{short_code}")
async def watch_page(request: Request, short_code: str):
    file_data = await files_col.find_one({"short_code": short_code})
    if not file_data:
        raise HTTPException(status_code=404, detail="Link not found or expired")
    
    return templates.TemplateResponse("watch.html", {
        "request": request,
        "file": file_data,
        "base_url": settings.BASE_URL
    })

@app.get("/dl/{short_code}")
@app.get("/stream/{short_code}")
async def stream_file(request: Request, short_code: str):
    file_data = await files_col.find_one({"short_code": short_code})
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    client = session_manager.get_client()
    
    try:
        # Fetch the message that contains the media
        msg = await client.get_messages(file_data['chat_id'], ids=file_data['message_id'])
        if not msg or not msg.media:
            raise HTTPException(status_code=404, detail="Media no longer available on Telegram")
        
        file = msg.media
        # Some media types are nested
        if hasattr(file, 'document'):
            file = file.document
        elif hasattr(file, 'photo'):
            file = file.photo
            
    except Exception as e:
        logger.error(f"Error fetching file: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving file from Telegram")

    return await get_streaming_response(
        client, 
        file=file,
        file_size=file_data['file_size'],
        filename=file_data['filename'],
        mime_type=file_data['mime_type'],
        request=request
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
