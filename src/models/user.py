"""
OOP - Inheritance & Encapsulation
SOLID - Open/Closed Principle (ขยายได้โดยไม่แก้ไข User)
หมายเหตุ: ไม่มีระบบสมาชิก/ล็อกอิน — ลูกค้าจองโดยระบุชื่อ-เบอร์เท่านั้น
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class User(ABC):
    """Base class - Inheritance (สำหรับขยายในอนาคตถ้ามีระบบสมาชิก)"""
    _name: str
    _phone: str
    _customer_id: str

    def __post_init__(self):
        if not self._name or not self._phone:
            raise ValueError("Name and phone are required")

    # Encapsulation - ใช้ property ป้องกันการเข้าถึงโดยตรง
    @property
    def name(self) -> str:
        return self._name

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @abstractmethod
    def get_discount_rate(self) -> float:
        """Polymorphism - สำหรับขยายถ้ามีระบบส่วนลดในอนาคต"""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._name}, {self._customer_id})"


class Customer(User):
    """ลูกค้าทั่วไป — จองโดยระบุชื่อ-เบอร์ (ไม่ล็อกอิน, ไม่มีระบบสมาชิก)"""
    def get_discount_rate(self) -> float:
        return 0.0
