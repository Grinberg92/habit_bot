from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    telegram_id: int
    username: str
    created_at: datetime
    
    @classmethod
    def from_row(cls, row: tuple):
        return cls(
            id = row[0],
            telegram_id = row[1],
            username = row[2],
            created_at = row[3]
        )