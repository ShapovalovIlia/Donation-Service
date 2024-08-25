from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from donation.domain.constants import ContributionStatus


@dataclass
class Contribution:
    status: ContributionStatus
    created_at: datetime
    status_updated_at: Optional[datetime]
