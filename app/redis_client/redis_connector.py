import logging

from redis import Redis

class RedisConnector:
    def __init__(self, host="redis", port=6379, db=0):
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