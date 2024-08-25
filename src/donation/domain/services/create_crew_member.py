from donation.domain.constants import CrewMembership
from donation.domain.value_objects import CrewMemberId
from donation.domain.entities import (
    CrewMember,
    Movie,
    Person,
)


class CreateCrewMember:
    def __call__(
        self,
        *,
        id: CrewMemberId,
        movie: Movie,
        person: Person,
        membership: CrewMembership,
    ) -> CrewMember:
        return CrewMember(
            id=id,
            movie_id=movie.id,
            person_id=person.id,
            membership=membership,
        )
