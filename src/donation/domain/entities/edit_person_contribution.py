from typing import Iterable, Optional
from dataclasses import dataclass
from datetime import date

from donation.domain.constants import Sex
from donation.domain.value_objects import (
    EditPersonContributionId,
    UserId,
    PersonId,
    PhotoUrl,
)
from donation.domain.maybe import Maybe
from .contribution import Contribution


@dataclass(slots=True)
class EditPersonContribution(Contribution):
    id: EditPersonContributionId
    author_id: UserId
    person_id: PersonId
    first_name: Maybe[str]
    last_name: Maybe[str]
    sex: Maybe[Sex]
    birth_date: Maybe[date]
    death_date: Maybe[Optional[date]]
    photos_to_add: Iterable[PhotoUrl]
