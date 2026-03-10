"""
SOLID - Single Responsibility, Dependency Inversion
ใช้ PricingStrategy (abstraction) แทน implementation โดยตรง
"""
from ..models.booking import Booking
from ..models.seat import Seat, SeatStatus
from ..models.user import User
from ..repositories.seat_repository import SeatRepository
from ..repositories.booking_repository import BookingRepository
from ..strategies.pricing import PricingStrategy, StandardPricing


class BookingService:
    """Business logic สำหรับการจอง"""
    def __init__(self, pricing_strategy: PricingStrategy = None):
        # Dependency Inversion - รับ abstraction ไม่ใช่ concrete class
        self._pricing = pricing_strategy or StandardPricing()

    def get_available_seats(self):
        return SeatRepository.get_available()

    def get_all_seats(self):
        return SeatRepository.get_all()

    def calculate_price(self, seat: Seat, hours: float, user: User) -> float:
        return self._pricing.calculate(seat, hours, user)

    def create_booking(self, user: User, seat: Seat, hours: float) -> Booking:
        if not seat.is_available:
            raise ValueError(f"ที่นั่ง {seat.name} ไม่ว่าง")
        if hours < 0.5 or hours > 12:
            raise ValueError("กรุณาระบุเวลา 0.5-12 ชั่วโมง")
        price = self.calculate_price(seat, hours, user)
        booking = Booking(
            booking_id=BookingRepository.generate_id(),
            user=user,
            seat=seat,
            duration_hours=hours,
            total_price=price,
        )
        seat.status = SeatStatus.RESERVED
        BookingRepository.add(booking)
        return booking

    def get_all_bookings(self):
        return BookingRepository.get_all()
