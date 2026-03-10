"""
Design Pattern - Repository Pattern
SOLID - Single Responsibility (จัดการข้อมูล seat เท่านั้น)
"""
from typing import List, Optional
from ..models.seat import Seat, SeatStatus, StandardSeat, PremiumSeat, PrivateRoomSeat


class SeatRepository:
    """จัดการ CRUD ของ Seat"""
    _seats: List[Seat] = []
    _initialized: bool = False

    @classmethod
    def _ensure_initialized(cls) -> None:
        if not cls._initialized:
            cls._seats = []
            # Premium Zone - 12 เครื่อง (บางเครื่องไม่ว่างสำหรับ demo)
            for i in range(1, 13):
                seat = PremiumSeat(f"P{i:02d}", f"เครื่องพรีเมียม {i}")
                if i in (5, 6, 7, 8, 9, 10, 12):
                    seat.status = SeatStatus.OCCUPIED
                cls._seats.append(seat)
            # Standard Zone - 30 เครื่อง
            for i in range(1, 31):
                cls._seats.append(StandardSeat(f"S{i:02d}", f"เครื่องที่ {i}"))
            # Private Room - 5 ห้อง (ไม่ใช่ VR)
            for i in range(1, 6):
                cls._seats.append(PrivateRoomSeat(f"R{i:02d}", f"ห้องส่วนตัว {i}"))
            cls._initialized = True

    @classmethod
    def get_all(cls) -> List[Seat]:
        cls._ensure_initialized()
        return cls._seats.copy()

    @classmethod
    def get_by_id(cls, seat_id: str) -> Optional[Seat]:
        cls._ensure_initialized()
        for seat in cls._seats:
            if seat.seat_id == seat_id:
                return seat
        return None

    @classmethod
    def get_available(cls) -> List[Seat]:
        cls._ensure_initialized()
        return [s for s in cls._seats if s.is_available]
