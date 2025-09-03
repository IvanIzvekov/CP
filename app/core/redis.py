# Пока без реального подключения
class Redis:
    async def get(self, key):
        return None
    async def set(self, key, value, ex=None):
        pass

redis_client = Redis()
