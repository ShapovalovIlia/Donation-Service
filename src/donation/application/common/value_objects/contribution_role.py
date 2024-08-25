from dataclasses import dataclass

from donation.domain import PersonId


@dataclass(frozen=True, slots=True)
class ContributionRole:
    person_id: PersonId
    character: str
    importance: int
    is_spoiler: bool
