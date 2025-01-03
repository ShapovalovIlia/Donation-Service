from dataclasses import dataclass
from typing import Iterable, Optional
from datetime import date

from donation.domain import (
    Sex,
    PersonId,
    PhotoUrl,
    Maybe,
)


@dataclass(frozen=True, slots=True)
class EditPersonCommand:
    person_id: PersonId
    first_name: Maybe[str]
    last_name: Maybe[str]
    sex: Maybe[Sex]
    birth_date: Maybe[date]
    death_date: Maybe[Optional[date]]
    photos_to_add: Iterable[PhotoUrl]
