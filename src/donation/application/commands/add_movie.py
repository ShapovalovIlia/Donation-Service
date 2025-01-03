from dataclasses import dataclass
from typing import Iterable, Optional
from datetime import date

from donation.domain import (
    Genre,
    MPAA,
    Country,
    Money,
    PhotoUrl,
)
from donation.application.common import (
    ContributionRole,
    ContributionWriter,
    ContributionCrewMember,
)


@dataclass(frozen=True, slots=True)
class AddMovieCommand:
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
    roles: Iterable[ContributionRole]
    writers: Iterable[ContributionWriter]
    crew: Iterable[ContributionCrewMember]
    photos: Iterable[PhotoUrl]
