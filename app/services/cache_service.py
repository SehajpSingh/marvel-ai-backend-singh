from redis.asyncio import Redis
from abc import ABC, abstractmethod
import os

class CacheInterface(ABC):
    @abstractmethod
    async def get(self, key: str): pass

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int = None): pass

# Concrete implementation
class RedisService(CacheInterface):
    def __init__(self, redis_client: Redis = None):
        # In Replit, Redis may not be available
        try:
            self.client = redis_client or Redis(
                host=os.getenv('REDIS_HOST', '0.0.0.0'),  # Use 0.0.0.0 for localhost in Replit
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True,
                socket_connect_timeout=2  # Short timeout
            )
            # Test the connection
            self.client.ping()
            from app.services.logger import setup_logger
            logger = setup_logger("redis_service")
            logger.info("Redis connection successful")
        except Exception as e:
            from app.services.logger import setup_logger
            logger = setup_logger("redis_service")
            logger.warning(f"Redis connection failed: {str(e)}. Using fallback cache.")
            self.client = None

    async def get(self, key: str):
        if self.client:
            try:
                return await self.client.get(key)
            except Exception as e:
                from app.services.logger import setup_logger
                logger = setup_logger("redis_service")
                logger.error(f"Redis get error for key {key}: {str(e)}")
                return None
        return None

    async def set(self, key: str, value: str, ttl: int = None):
        if self.client:
            try:
                return await self.client.set(key, value, ex=ttl)
            except Exception as e:
                from app.services.logger import setup_logger
                logger = setup_logger("redis_service")
                logger.error(f"Redis set error for key {key}: {str(e)}")
                return False
        return False