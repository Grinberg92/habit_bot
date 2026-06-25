from dataclasses import dataclass
from datetime import datetime

@dataclass
class HabitCompletion:
    habit_id: int
    created_at: datetime

    @classmethod
    def from_row(cls, row: tuple):
        return cls(
            habit_id=row[0],
            created_at=row[1],
        )