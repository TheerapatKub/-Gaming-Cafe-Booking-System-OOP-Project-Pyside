# สคริปต์วิดีโอนำเสนอโปรเจกต์ (10-15 นาที)

> ใช้เป็นแนวทางในการถ่ายวิดีโอและอธิบาย สามารถตัดต่อหรือปรับประโยคให้กระชับได้

---

## ส่วนที่ 1: บทนำ (ประมาณ 1-2 นาที)

### กล่าวเปิด

> "สวัสดีครับ/ค่ะ วันนี้เราจะนำเสนอโปรเจกต์วิชาการเขียนโปรแกรมเชิงวัตถุ ชื่อโปรเจกต์ **Gaming Cafe Booking System** คือระบบจองเครื่องคอมพิวเตอร์ในร้านเกม พัฒนาด้วย PySide6 เป็นแอปพลิเคชัน Desktop"

### แนะนำทีม

> "ทีมของเราประกอบด้วย [ชื่อสมาชิก 1] ทำหน้าที่ [เช่น ดูแล Models และ OOP structure] และ [ชื่อสมาชิก 2] ทำหน้าที่ [เช่น ดูแล UI และ Services]"

---

## ส่วนที่ 2: Clone และติดตั้ง (ประมาณ 2-3 นาที)

### ขั้นตอนที่แสดงบนหน้าจอ

1. เปิด Terminal
2. พิมพ์:
   ```bash
   git clone https://github.com/TheerapatKub/-Gaming-Cafe-Booking-System-OOP-Project-Pyside.git
   cd "-Gaming-Cafe-Booking-System-OOP-Project-Pyside"
   ```
3. สร้าง virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. ติดตั้ง dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. รันโปรแกรม:
   ```bash
   python main.py
   ```

### ข้อความที่พูด

> "เราจะเริ่มจาก clone repository จาก GitHub ตามขั้นตอนใน README ติดตั้ง virtual environment และ pip install จาก requirements.txt จากนั้นรัน python main.py โปรแกรมจะเปิดขึ้นมา"

---

## ส่วนที่ 3: Demo การใช้งาน (ประมาณ 3-4 นาที)

### สิ่งที่ต้องแสดง

| ลำดับ | การกระทำ | ข้อความที่พูด |
|------|----------|----------------|
| 1 | แสดงหน้าต่างหลัก มี 3 แท็บ | "โปรแกรมมี 3 แท็บหลักคือ จองเครื่อง รายการเครื่อง และประวัติการจอง" |
| 2 | ไปที่แท็บ "รายการเครื่อง" | "ในรายการเครื่องจะเห็นเครื่องมาตรฐาน พรีเมียม และ VR พร้อมสถานะว่าว่างหรือจองแล้ว" |
| 3 | กลับไปแท็บ "จองเครื่อง" | "เมื่อจะจอง กรอกชื่อ เบอร์โทร เลือกประเภทสมาชิก ทั่วไปหรือ VIP" |
| 4 | เลือกเครื่อง ว่าง ชั่วโมง แล้วกดจอง | "เลือกเครื่องที่ว่าง ระบุจำนวนชั่วโมง แล้วกดจองเลย" |
| 5 | แสดง popup ยืนยันการจอง | "ระบบคำนวณราคาให้ โดย VIP จะได้ส่วนลด 15 เปอร์เซ็นต์" |
| 6 | ไปแท็บประวัติ | "เราสามารถดูประวัติการจองทั้งหมดได้ที่แท็บนี้" |

---

## ส่วนที่ 4: อธิบายโค้ด - OOP และ SOLID (ประมาณ 5-7 นาที)

### 4.1 Inheritance (1 นาที)

**เปิดไฟล์ `src/models/user.py`**

> "เราใช้ Inheritance อย่างชัดเจน คลาส User เป็น base class มี RegularMember และ VIPMember สืบทอดมา โดยแต่ละคลาสมีเมธอด get_discount_rate ที่คืนค่าต่างกัน สมาชิกทั่วไป 0% VIP 15%"

**เปิดไฟล์ `src/models/seat.py`**

> "ส่วน Seat ก็เช่นกัน มี StandardSeat PremiumSeat และ VRSeat สืบทอดจาก Seat แต่ละประเภทมีราคาต่อชั่วโมงต่างกัน"

---

### 4.2 Encapsulation (30 วินาที)

**ชี้ที่ property ใน user.py หรือ seat.py**

> "Encapsulation เราใช้ underscore _name _phone เป็น private attribute และให้เข้าถึงผ่าน property เท่านั้น"

---

### 4.3 Polymorphism (30 วินาที)

> "Polymorphism เกิดขึ้นที่เมธอด get_discount_rate และ get_base_price_per_hour เมื่อเรียกจาก object ชนิดต่างกัน จะได้ผลลัพธ์ต่างกันตามประเภท"

---

### 4.4 Composition (30 วินาที)

**เปิดไฟล์ `src/models/booking.py`**

> "Composition ใช้ใน Booking class ที่ประกอบด้วย User, Seat, duration และ total_price คือรวมหลาย object เข้าด้วยกัน"

---

### 4.5 SOLID Principles (1-2 นาที)

| หลักการ | ไฟล์ที่อ้าง | ข้อความสั้นๆ |
|---------|-------------|--------------|
| **S**ingle Responsibility | `seat_repository.py`, `booking_repository.py` | "Repository แต่ละตัวดูแลข้อมูลแยกส่วนกัน" |
| **O**pen/Closed | `user.py`, `seat.py` | "เพิ่ม RegularMember หรือ PremiumSeat ใหม่ได้โดยไม่แก้ไข base class" |
| **L**iskov Substitution | การใช้ Seat แทน StandardSeat | "ทุก subclass ของ Seat สามารถใช้แทน Seat ได้" |
| **D**ependency Inversion | `booking_service.py` | "BookingService รับ PricingStrategy เป็น abstraction ไม่ผูกกับ implementation โดยตรง" |

---

### 4.6 Design Patterns (1 นาที)

**เปิด `src/strategies/pricing.py`**

> "เราใช้ Strategy Pattern สำหรับการคำนวณราคา PricingStrategy เป็น interface มี StandardPricing และ VIPPricing เป็น implementation"

**ชี้ SeatStatus ใน seat.py**

> "State Pattern ใช้กับ SeatStatus คือ enum แทนสถานะต่างๆ ของเก้าอี้"

**เปิด `src/ui/main_window.py`**

> "main_window.py เป็น PySide6 UI สร้าง MainWindow มี 3 แท็บ ใช้ QTableWidget แสดงข้อมูล และเชื่อมกับ BookingService"

---

## ส่วนที่ 5: สรุป (ประมาณ 30 วินาที - 1 นาที)

> "สรุป โปรเจกต์ของเราเป็นระบบจองเครื่องร้านเกมด้วย PySide6 Desktop GUI ใช้ OOP ทั้ง Inheritance Polymorphism Encapsulation Composition ตามหลัก SOLID และ Design Patterns เช่น Strategy Repository และ State ขอบคุณที่รับชมครับ/ค่ะ"

---

## เคล็ดลับการถ่ายวิดีโอ

- บันทึกหน้าจอ (Screen record) แยกจากส่วนพูด แล้วตัดต่อรวมกัน
- ใช้ subtitle หรือ text overlay ช่วยเน้นจุดสำคัญ
- ถ้าบางส่วนยาวเกิน ให้ตัดหรือพูดสรุปสั้นๆ
- ตรวจสอบให้ audio ชัด และไมค์ไม่ดังเกินไป

---

## สรุปเวลาโดยรวม (ประมาณ)

| ส่วน | เวลา |
|------|------|
| บทนำ + แนะนำทีม | 1-2 นาที |
| Clone + ติดตั้ง + รัน | 2-3 นาที |
| Demo การใช้งาน | 3-4 นาที |
| อธิบายโค้ด (OOP, SOLID, Patterns) | 5-7 นาที |
| สรุป | 0.5-1 นาที |
| **รวม** | **ประมาณ 12-17 นาที** |

ปรับลดหรือขยายแต่ละส่วนให้อยู่ภายใน 10-15 นาทีตามที่กำหนด
