from typing import Protocol, Optional

from donation.domain import (
    AddMovieContributionId,
    AddMovieContribution,
)


class AddMovieContributionGateway(Protocol):
    async def acquire_by_id(
        self,
        id: AddMovieContributionId,
    ) -> Optional[AddMovieContribution]:
        raise NotImplementedError

    async def save(self, contribution: AddMovieContribution) -> None:
        raise NotImplementedError

    async def update(self, contribution: AddMovieContribution) -> None:
        raise NotImplementedError
