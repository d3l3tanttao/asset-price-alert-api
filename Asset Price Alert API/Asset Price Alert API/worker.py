from redis import Redis
from rq import SimpleWorker

from app.config import get_settings


settings = get_settings()

redis_connection = Redis.from_url(settings.redis_url)


if __name__ == "__main__":
    worker = SimpleWorker(
        queues=["price-checks"],
        connection=redis_connection,
    )

    worker.work()