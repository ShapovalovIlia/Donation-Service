from donation.domain.constants import Writing
from donation.domain.value_objects import WriterId
from donation.domain.entities import (
    Writer,
    Movie,
    Person,
)


class CreateWriter:
    def __call__(
        self,
        *,
        id: WriterId,
        movie: Movie,
        person: Person,
        writing: Writing,
    ) -> Writer:
        return Writer(
            id=id,
            movie_id=movie.id,
            person_id=person.id,
            writing=writing,
        )
