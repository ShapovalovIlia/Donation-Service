from dishka import Provider, Scope

from donation.infra.database import mongodb_config_from_env
from donation.infra.message_broker import rabbitmq_config_from_env


def event_consumer_configs_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(mongodb_config_from_env)
    provider.provide(rabbitmq_config_from_env)

    return provider
