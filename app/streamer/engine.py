import math
from telethon import TelegramClient
from telethon.tl.types import Document, Photo
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse
import logging

logger = logging.getLogger(__name__)

async def media_streamer(client: TelegramClient, file, start: int, end: int, chunk_size: int = 4 * 1024 * 1024):
    """
    Generator that yields chunks of media from Telegram.
    Highly optimized and precise for streaming.
    """
    total_to_send = end - start + 1
    bytes_sent = 0
    
    try:
        # iter_download is the most compatible way to stream chunks
        async for chunk in client.iter_download(
            file,
            offset=start,
            request_size=chunk_size
        ):
            if bytes_sent >= total_to_send:
                break
                
            # If the last chunk is larger than what we need, slice it
            if bytes_sent + len(chunk) > total_to_send:
                chunk = chunk[:total_to_send - bytes_sent]
            
            yield bytes(chunk)
            bytes_sent += len(chunk)
            
            if bytes_sent >= total_to_send:
                break
                
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Streaming error: {e}")

def get_range_header(request: Request, file_size: int):
    range_header = request.headers.get("Range")
    if not range_header:
        return 0, file_size - 1

    try:
        range_val = range_header.replace("bytes=", "")
        start_str, end_str = range_val.split("-")
        start = int(start_str) if start_str else 0
        end = int(end_str) if end_str else file_size - 1
    except ValueError:
        return 0, file_size - 1

    return start, min(end, file_size - 1)

async def get_streaming_response(client: TelegramClient, file, file_size: int, filename: str, mime_type: str, request: Request):
    start, end = get_range_header(request, file_size)
    
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
        "Content-Type": mime_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }

    status_code = 206 if request.headers.get("Range") else 200

    return StreamingResponse(
        media_streamer(client, file, start, end),
        status_code=status_code,
        headers=headers
    )
