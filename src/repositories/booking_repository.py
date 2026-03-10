"""
Design Pattern - Repository Pattern
SOLID - Single Responsibility
"""
from typing import List
from ..models.booking import Booking


class BookingRepository:
    """จัดการข้อมูล Booking"""
    _bookings: List[Booking] = []
    _next_id: int = 1

    @classmethod
    def add(cls, booking: Booking) -> None:
        cls._bookings.append(booking)

    @classmethod
    def get_all(cls) -> List[Booking]:
        return cls._bookings.copy()

    @classmethod
    def generate_id(cls) -> str:
        bid = f"B{cls._next_id:04d}"
        cls._next_id += 1
        return bid
