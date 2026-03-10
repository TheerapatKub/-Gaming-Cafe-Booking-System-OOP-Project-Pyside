"""
OOP - Inheritance & Encapsulation
SOLID - Open/Closed Principle (ขยายได้โดยไม่แก้ไข User)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class User(ABC):
    """Base class - Inheritance"""
    _name: str
    _phone: str
    _member_id: str

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
    def member_id(self) -> str:
        return self._member_id

    @abstractmethod
    def get_discount_rate(self) -> float:
        """Polymorphism - แต่ละประเภทมี discount ต่างกัน"""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._name}, {self._member_id})"


class RegularMember(User):
    """Inheritance - สมาชิกทั่วไป (discount 0%)"""
    def get_discount_rate(self) -> float:
        return 0.0


class VIPMember(User):
    """Inheritance - สมาชิก VIP (discount 15%)"""
    def get_discount_rate(self) -> float:
        return 0.15
