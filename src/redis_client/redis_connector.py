import logging
import os

from redis import Redis

class RedisConnector:
    def __init__(self, host=None, port=None, db=None):
        host = "redis"  # Use the service name from Docker Compose
        # host = host or "127.0.0.1"
        port = 6379
        db = 0

        try:
            self.redis = Redis(host=host, port=port, db=db)
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            
    def get_redis(self):
        """
        Returns the Redis instance
        """
        logging.info('Getting Redis client')
        return self.redis