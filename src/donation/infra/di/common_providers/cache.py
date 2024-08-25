from dishka import Provider, Scope

from donation.infra.cache import PermissionsCache


def cache_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(PermissionsCache)

    return provider
