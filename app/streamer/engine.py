import math
from telethon import TelegramClient
from telethon.tl.types import Document, Photo
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse
import logging

logger = logging.getLogger(__name__)

async def media_streamer(client: TelegramClient, file, start: int, end: int, chunk_size: int = 1024 * 1024):
    """
    Parallel media streamer that fetches multiple chunks from Telegram simultaneously.
    This bypasses sequential bottlenecks and maxes out available bandwidth.
    """
    import asyncio
    total_to_send = end - start + 1
    bytes_sent = 0
    concurrency = 8  # Number of parallel requests
    
    # Divide the requested range into smaller chunks for parallel fetching
    offsets = list(range(start, end + 1, chunk_size))
    
    for i in range(0, len(offsets), concurrency):
        batch = offsets[i:i + concurrency]
        
        # Helper to fetch a single chunk with retries
        async def fetch_part(offset):
            # Calculate remaining size to avoid over-fetching
            remaining = end - offset + 1
            current_chunk_size = min(chunk_size, remaining)
            
            for attempt in range(3):
                try:
                    # Use download_file for precise offset/size fetching
                    return await client.download_file(
                        file, 
                        offset=offset, 
                        file_size=current_chunk_size
                    )
                except Exception:
                    if attempt == 2: return None  # Failed after 3 attempts
                    await asyncio.sleep(0.5)  # Quick retry
            return None

        # Fetch batch in parallel
        tasks = [fetch_part(offset) for offset in batch]
        chunks = await asyncio.gather(*tasks)
        
        for chunk in chunks:
            if not chunk: continue
            
            if bytes_sent + len(chunk) > total_to_send:
                chunk = chunk[:total_to_send - bytes_sent]
            
            yield bytes(chunk)
            bytes_sent += len(chunk)
            
            if bytes_sent >= total_to_send:
                break

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
