from dataclasses import dataclass
from datetime import datetime

from donation.domain.constants import Achieved
from donation.domain.value_objects import (
    AchievementId,
    UserId,
)


@dataclass(slots=True)
class Achievement:
    id: AchievementId
    user_id: UserId
    achieved: Achieved
    achieved_at: datetime
