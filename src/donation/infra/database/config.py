import os
from dataclasses import dataclass
from typing import Optional

from donation.infra.get_env import env_var_by_key


def mongodb_config_from_env() -> "MongoDBConfig":
    port_as_str = os.getenv("MONGODB_PORT")
    if port_as_str:
        port = int(port_as_str)
    else:
        port = None

    return MongoDBConfig(
        url=env_var_by_key("MONGODB_URL"),
        port=port,
    )


@dataclass(frozen=True, slots=True)
class MongoDBConfig:
    url: str
    port: Optional[int]
