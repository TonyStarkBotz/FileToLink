from app.cache.redis_client import redis_client
import time

async def check_rate_limit(user_id: int, limit: int = 5, period: int = 60):
    """
    Check if a user has exceeded the rate limit.
    limit: number of requests
    period: time window in seconds
    """
    key = f"rate_limit:{user_id}"
    try:
        current_count = await redis_client.get(key)
        
        if current_count and int(current_count) >= limit:
            return False
            
        async with redis_client.pipeline(transaction=True) as pipe:
            await pipe.incr(key)
            await pipe.expire(key, period)
            await pipe.execute()
    except Exception as e:
        # If Redis is down, we allow the request but log the error
        import logging
        logging.getLogger(__name__).warning(f"Redis rate limit check failed: {e}")
        
    return True
