from dataclasses import dataclass

from donation.domain.constants import Writing
from donation.domain.value_objects import (
    WriterId,
    MovieId,
    PersonId,
)


@dataclass(slots=True)
class Writer:
    id: WriterId
    movie_id: MovieId
    person_id: PersonId
    writing: Writing
