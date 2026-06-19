from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    user_id: int
    title: str
    created_at: datetime
    is_done: bool
    
    @classmethod
    def from_row(cls, row: tuple):
        return cls(
            id = row[0],
            user_id = row[1],
            title = row[2],
            created_at = row[3],
            is_done = row[4],
        )