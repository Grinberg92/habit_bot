from dataclasses import dataclass
from datetime import datetime, time

@dataclass
class Habit:
    id: int
    user_id: int
    title: str
    reminder_time: time
    is_active: bool
    created_at: datetime

    @classmethod
    def from_row(cls, row: tuple):
        return cls(
            id=row[0],
            user_id=row[1],
            title=row[2],
            reminder_time=row[3],
            is_active=row[4],
            created_at=row[5],
        )