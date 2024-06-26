from dataclasses import dataclass
from os import getenv


@dataclass
class NatsConfig:
    broker_url: str
    bucket_name: str
    ttl: int

    def from_env() -> "NatsConfig":
        broker_url = getenv("NATS_URL", "nats://localhost:4222")
        bucket_name = getenv("NATS_OBJECT_BUCKET", "storage")
        ttl = int(getenv("NATS_OBJECT_TTL", "60"))
        return NatsConfig(broker_url, bucket_name, ttl)


@dataclass
class MinioConfig:
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str

    @staticmethod
    def from_env() -> "MinioConfig":
        access_key = getenv("ACCESS_KEY", "minioadmin")
        secret_key = getenv("SECRET_KEY", "minioadmin")
        endpoint_url = getenv("MINIO_URL_INNER", "http://localhost:9000")
        bucket_name = getenv("BUCKET_NAME", "storage")
        return MinioConfig(access_key, secret_key, endpoint_url, bucket_name)


@dataclass
class Config:
    nats_config: NatsConfig
    minio_config: MinioConfig

    @staticmethod
    def from_env() -> "Config":
        return Config(
            nats_config=NatsConfig.from_env(), minio_config=MinioConfig.from_env()
        )


config = Config.from_env()
