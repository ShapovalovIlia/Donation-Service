from dishka import Provider, Scope

from donation.infra.operation_id.default import (
    default_operation_id_factory,
)


def cli_operation_id_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(default_operation_id_factory)

    return provider
