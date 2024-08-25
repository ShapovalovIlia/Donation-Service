from typing import Protocol

from donation.domain import UserId


class IdentityProvider(Protocol):
    async def user_id(self) -> UserId:
        raise NotImplementedError

    async def permissions(self) -> int:
        raise NotImplementedError
