from dataclasses import dataclass
from datetime import datetime

from donation.domain import EditMovieContributionId


@dataclass(frozen=True, slots=True)
class AcceptMovieEditingCommand:
    contribution_id: EditMovieContributionId
    accepted_at: datetime
