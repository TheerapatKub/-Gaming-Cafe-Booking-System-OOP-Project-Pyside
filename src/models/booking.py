"""
OOP - Composition
Booking ประกอบด้วย User + Seat + duration
"""
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .seat import Seat


@dataclass
class Booking:
    """Composition - รวม User, Seat, duration เข้าด้วยกัน"""
    booking_id: str
    user: "User"
    seat: "Seat"
    duration_hours: float
    total_price: float
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"Booking#{self.booking_id}: {self.user.name} @ {self.seat.name} ({self.duration_hours} ชม.)"
