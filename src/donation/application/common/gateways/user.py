from typing import Protocol, Optional

from donation.domain import UserId, User


class UserGateway(Protocol):
    async def by_id(self, id: UserId) -> Optional[User]:
        raise NotImplementedError

    async def by_name(self, name: str) -> Optional[User]:
        raise NotImplementedError

    async def by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    async def by_telegram(self, telegram: str) -> Optional[User]:
        raise NotImplementedError

    async def acquire_by_id(self, id: UserId) -> Optional[User]:
        raise NotImplementedError

    async def save(self, user: User) -> None:
        raise NotImplementedError

    async def update(self, user: User) -> None:
        raise NotImplementedError
