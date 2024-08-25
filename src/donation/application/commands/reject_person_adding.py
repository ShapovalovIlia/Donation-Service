from dataclasses import dataclass
from datetime import datetime

from donation.domain import AddPersonContributionId


@dataclass(frozen=True, slots=True)
class RejectPersonAddingCommand:
    contribution_id: AddPersonContributionId
    rejected_at: datetime
