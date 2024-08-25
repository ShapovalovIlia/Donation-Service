from typing import Iterable, Optional
from dataclasses import dataclass
from datetime import date

from donation.domain.constants import Sex
from donation.domain.value_objects import (
    AddPersonContributionId,
    UserId,
    PhotoUrl,
)
from .contribution import Contribution


@dataclass(slots=True)
class AddPersonContribution(Contribution):
    id: AddPersonContributionId
    author_id: UserId
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
    photos: Iterable[PhotoUrl]
