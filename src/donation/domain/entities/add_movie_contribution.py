from typing import Iterable, Optional
from dataclasses import dataclass
from datetime import date

from donation.domain.constants import (
    Genre,
    MPAA,
)
from donation.domain.value_objects import (
    AddMovieContributionId,
    UserId,
    MovieRole,
    MovieWriter,
    MovieCrewMember,
    Country,
    Money,
    PhotoUrl,
)
from .contribution import Contribution


@dataclass(slots=True)
class AddMovieContribution(Contribution):
    id: AddMovieContributionId
    author_id: UserId
    eng_title: str
    original_title: str
    summary: str
    description: str
    release_date: date
    countries: Iterable[Country]
    genres: Iterable[Genre]
    mpaa: MPAA
    duration: int
    budget: Optional[Money]
    revenue: Optional[Money]
    roles: Iterable[MovieRole]
    writers: Iterable[MovieWriter]
    crew: Iterable[MovieCrewMember]
    photos: Iterable[PhotoUrl]
