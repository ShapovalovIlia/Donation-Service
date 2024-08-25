from dataclasses import dataclass

from donation.infra.get_env import env_var_by_key


def redis_config_from_env() -> "RedisConfig":
    return RedisConfig(
        url=env_var_by_key("REDIS_URL"),
    )


@dataclass(frozen=True, slots=True)
class RedisConfig:
    url: str
