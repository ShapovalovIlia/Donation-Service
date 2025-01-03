from dataclasses import dataclass

from donation.infra.get_env import env_var_by_key


def rabbitmq_config_from_env() -> "RabbitMQConfig":
    return RabbitMQConfig(
        url=env_var_by_key("RABBITMQ_URL"),
    )


@dataclass(frozen=True, slots=True)
class RabbitMQConfig:
    url: str
