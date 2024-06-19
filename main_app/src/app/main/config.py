from dataclasses import dataclass
from os import getenv


@dataclass
class Config:
    broker_url: str
    bucket_name: str
    ttl: int

    @staticmethod
    def from_env() -> "Config":
        broker_url = getenv("NATS_URL", "nats://localhost:4222")
        bucket_name = getenv("BUCKET_NAME", "storage")
        ttl = int(getenv("TTL", "60"))
        return Config(broker_url, bucket_name, ttl)
