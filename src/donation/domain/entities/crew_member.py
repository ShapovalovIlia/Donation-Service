from dataclasses import dataclass

from donation.domain.constants import CrewMembership
from donation.domain.value_objects import (
    CrewMemberId,
    MovieId,
    PersonId,
)


@dataclass(slots=True)
class CrewMember:
    id: CrewMemberId
    movie_id: MovieId
    person_id: PersonId
    membership: CrewMembership
