"""
Design Pattern - Strategy Pattern
SOLID - Open/Closed (เพิ่ม pricing ใหม่ได้ไม่ต้องแก้ไขเดิม)
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.user import User
    from ..models.seat import Seat


class PricingStrategy(ABC):
    """Strategy Pattern - Interface สำหรับการคำนวณราคา"""
    @abstractmethod
    def calculate(self, seat: "Seat", hours: float, user: "User") -> float:
        pass


class StandardPricing(PricingStrategy):
    """ราคาปกติ (ไม่มี discount)"""
    def calculate(self, seat: "Seat", hours: float, user: "User") -> float:
        base = seat.get_base_price_per_hour() * hours
        discount = base * user.get_discount_rate()
        return max(0, base - discount)


class VIPPricing(PricingStrategy):
    """ราคาสำหรับ VIP (มี discount เพิ่ม)"""
    def calculate(self, seat: "Seat", hours: float, user: "User") -> float:
        base = seat.get_base_price_per_hour() * hours
        discount_rate = user.get_discount_rate() + 0.05  # VIP ได้เพิ่มอีก 5%
        return max(0, base * (1 - discount_rate))
