from dataclasses import dataclass

from donation.domain import CrewMembership, PersonId


@dataclass(frozen=True, slots=True)
class ContributionCrewMember:
    person_id: PersonId
    membership: CrewMembership
