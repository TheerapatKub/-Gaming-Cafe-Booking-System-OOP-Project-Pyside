"""
OOP - Inheritance & Polymorphism
SOLID - Open/Closed, Liskov Substitution
Design Pattern - State (SeatStatus)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class SeatStatus(Enum):
    """State Pattern - สถานะของเก้าอี้"""
    AVAILABLE = "ว่าง"
    OCCUPIED = "กำลังใช้งาน"
    RESERVED = "จองแล้ว"
    MAINTENANCE = "ซ่อมบำรุง"


@dataclass
class Seat(ABC):
    """Base class - Inheritance"""
    _seat_id: str
    _name: str
    _status: SeatStatus = SeatStatus.AVAILABLE

    # Encapsulation
    @property
    def seat_id(self) -> str:
        return self._seat_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> SeatStatus:
        return self._status

    @status.setter
    def status(self, value: SeatStatus) -> None:
        self._status = value

    @property
    def is_available(self) -> bool:
        return self._status == SeatStatus.AVAILABLE

    @abstractmethod
    def get_base_price_per_hour(self) -> float:
        """Polymorphism - ราคาต่อชั่วโมงต่างกันตามประเภท"""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._seat_id}: {self._name})"


class StandardSeat(Seat):
    """Inheritance - เครื่องมาตรฐาน 40 บาท/ชม."""
    def get_base_price_per_hour(self) -> float:
        return 40.0


class PremiumSeat(Seat):
    """Inheritance - เครื่องสเปกสูง 80 บาท/ชม."""
    def get_base_price_per_hour(self) -> float:
        return 80.0


class VRSeat(Seat):
    """Inheritance - ห้อง Private Room 250 บาท/ชม."""
    def get_base_price_per_hour(self) -> float:
        return 250.0
