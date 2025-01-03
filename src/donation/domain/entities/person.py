from dataclasses import dataclass
from typing import Optional
from datetime import date

from donation.domain.constants import Sex
from donation.domain.value_objects import PersonId


@dataclass(slots=True)
class Person:
    id: PersonId
    first_name: str
    last_name: str
    sex: Sex
    birth_date: date
    death_date: Optional[date]
