from dishka import Provider, Scope

from donation.infra.database import MongoDBLockFactory


def mongodb_lock_factory_provider_factory() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(MongoDBLockFactory)

    return provider
