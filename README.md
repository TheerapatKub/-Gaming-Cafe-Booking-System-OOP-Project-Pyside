# 🎮 Gaming Cafe Booking System

> ระบบจองเครื่องร้านเกมสุดเจ๋ง — โปรเจกต์วิชาการเขียนโปรแกรมเชิงวัตถุ (OOP) Final Team Project ✨

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Desktop%20GUI-41CD52?style=flat&logo=qt&logoColor=white)

---

## 📋 รายการส่งงาน (Submission Requirements)

โปรเจกต์นี้ตรงตามข้อกำหนดการส่งงานครบถ้วน:

| รายการ | สถานะ | รายละเอียด |
|--------|--------|-------------|
| **Source Code ทั้งหมด** | ✅ | โครงสร้างโปรเจกต์ครบใน Repository |
| **README.md** | ✅ | มีชื่อทีม, สมาชิก และวิธีการติดตั้ง/ใช้งาน |
| **requirements.txt** | ✅ | สำหรับติดตั้ง Library ที่เกี่ยวข้อง (PySide6) |
| **pyproject.toml** | ✅ | สำหรับติดตั้ง Library ที่เกี่ยวข้อง |

---

## 👥 ข้อมูลทีม

| รายการ | รายละเอียด |
|--------|-------------|
| **ชื่อทีม** | T Olio |
| **สมาชิก** | นายธีรภัทร พิกุลศรี (รหัส 68114540308) |
| **Framework** | PySide6 (Desktop GUI) |

---

## 🚀 ความสามารถของระบบ

- 🖥️ **จองเครื่อง/เก้าอี้** เล่นร้านเกม
- ⚡ **เลือกประเภทเครื่อง**: Standard (40฿/ชม.) | Premium (80฿/ชม.) | Private Room (250฿/ชม.)
- 📋 **ดูสถานะเครื่อง** และประวัติการจอง

### หน้าจอในโปรแกรม (4 หน้า)

| หน้า | รายละเอียด |
|------|-------------|
| **1. ฟอร์มจอง** | เลือกเวลา, โซน, เครื่อง, กรอกชื่อ-เบอร์, เลือกชำระเงิน (สแกนจ่าย/จ่ายที่ร้าน) มีสรุปการจองและราคา real-time ทางขวามือ |
| **2. QR Code** | แสดงเมื่อเลือกสแกนจ่าย — ยอดชำระ, ปุ่มยืนยันการโอนเงิน |
| **3. หน้าสำเร็จ** | แสดงรหัสจอง GC-XXXX, ใบเสร็จ, แจ้งชื่อที่เคาน์เตอร์ |
| **4. ประวัติการจอง** | รายการจองทั้งหมด พร้อมรหัส สถานะ (ชำระแล้ว/รอชำระ) โซน เครื่อง ชั่วโมง ยอดเงิน |

### โซนเครื่อง

| โซน | สเปก | ราคา |
|-----|------|------|
| **Standard** | จอ 144Hz / การ์ดจอ RTX 3060 | 40฿/ชม. |
| **Premium** | จอ 240Hz / การ์ดจอ RTX 4070 | 80฿/ชม. |
| **Private Room** | ห้องส่วนตัว / จอคู่ 360Hz (ไม่ใช่ VR) | 250฿/ชม. |

---

## 📦 Requirements (Library ที่เกี่ยวข้อง)

ติดตั้งได้จาก `requirements.txt` หรือ `pyproject.toml`

| Library | เวอร์ชัน | ใช้สำหรับ |
|---------|----------|-----------|
| **PySide6** | >= 6.5.0 | Desktop GUI (Qt for Python) |

```txt
# requirements.txt
PySide6>=6.5.0
```

---

## ⚙️ การติดตั้งและใช้งาน

### การติดตั้ง

```bash
# 1️⃣ Clone repository
git clone https://github.com/TheerapatKub/-Gaming-Cafe-Booking-System-OOP-Project-Pyside.git
cd "-Gaming-Cafe-Booking-System-OOP-Project-Pyside"

# 2️⃣ สร้าง virtual environment (แนะนำ)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# 3️⃣ ติดตั้ง dependencies
pip install -r requirements.txt

# 4️⃣ รันโปรแกรม
python main.py
```

---

## 📖 วิธีการใช้งาน

หลังรัน `python main.py` โปรแกรมจะเปิดหน้าต่าง **Gaming Cafe - จองเครื่อง** สามารถใช้งานได้ดังนี้:

### ขั้นตอนการจองเครื่อง

| ขั้นตอน | การดำเนินการ |
|---------|---------------|
| **1️⃣ เลือกเวลา** | เลือก "จองตอนนี้" หรือ "จองล่วงหน้า" (ถ้าจองล่วงหน้าต้องเลือกวันที่และเวลา) |
| **2️⃣ กำหนดชั่วโมง** | เลือกจำนวนชั่วโมงที่ต้องการ (1–24 ชม.) |
| **3️⃣ เลือกโซน** | กดเลือกโซน **Standard** (40฿/ชม.) · **Premium** (80฿/ชม.) · **Private Room** (250฿/ชม.) |
| **4️⃣ เลือกเครื่อง** | กดเลือกหมายเลขเครื่องที่ว่าง (ปุ่มขีดทับ = ไม่ว่าง) |
| **5️⃣ กรอกข้อมูล** | กรอกชื่อ-นามสกุล และเบอร์โทรศัพท์ |
| **6️⃣ เลือกชำระเงิน** | เลือก **สแกนจ่าย** หรือ **จ่ายที่ร้าน** |
| **7️⃣ ยืนยัน** | กดปุ่ม "ดำเนินการชำระเงิน" เพื่อยืนยันการจอง |

### ฟีเจอร์อื่นๆ

- **📋 ประวัติการจอง** — กดปุ่มด้านขวาบนเพื่อดูประวัติการจองทั้งหมด
- **🏠 กลับหน้าแรก** — กด "Gaming Cafe" ที่มุมซ้ายบนเพื่อจองเครื่องใหม่
- **💳 สแกนจ่าย** — ถ้าเลือกชำระด้วย QR โปรแกรมจะแสดงหน้า QR Code กด "ยืนยันการโอนเงิน" เพื่อไปหน้าสำเร็จ
- **👤 จ่ายที่ร้าน** — กด "ยืนยันการจอง" ไปหน้าสำเร็จทันที สถานะจะเป็น "รอชำระที่ร้าน"
- **รหัสการจอง** — ใช้รูปแบบ GC-XXXX (เช่น GC-0001)

> 💡 ราคาจะคำนวณและแสดงทางขวามือแบบ real-time เมื่อเลือกโซนและเครื่องแล้ว

---

## 📁 โครงสร้างโปรเจกต์

```
📂 project
├── 🐍 main.py                 # Entry point (PySide6)
├── 📂 assets/icons/           # ไอคอน (optional)
├── 📄 requirements.txt
├── 📄 pyproject.toml
├── 📄 README.md
└── 📂 src/
    ├── 📂 models/             # OOP: User, Seat, Booking
    ├── 📂 strategies/         # Design Pattern: Strategy (Pricing)
    ├── 📂 repositories/       # Repository Pattern
    ├── 📂 services/           # Business Logic
    └── 📂 ui/                 # PySide6 GUI
```

---

## 🧠 การประยุกต์ใช้ OOP และ SOLID

| หลักการ | การใช้งานในโค้ด |
|---------|------------------|
| **🏛️ Inheritance** | User → Customer / Seat → StandardSeat, PremiumSeat, PrivateRoomSeat |
| **🌀 Polymorphism** | get_discount_rate(), get_base_price_per_hour() |
| **🔒 Encapsulation** | property สำหรับ _name, _status ฯลฯ |
| **🧩 Composition** | Booking ประกอบด้วย User + Seat + duration |
| **📌 SOLID - S** | SeatRepository, BookingRepository แยกหน้าที่ |
| **🔓 SOLID - O** | เพิ่มประเภท Seat/User ใหม่ได้ไม่แก้ไขเดิม |
| **🔌 SOLID - D** | BookingService รับ PricingStrategy (abstraction) |

---

## 🎯 Design Patterns

| Pattern | รายละเอียด |
|---------|-------------|
| **⚙️ Strategy** | PricingStrategy สำหรับคำนวณราคา |
| **📦 Repository** | SeatRepository, BookingRepository |
| **🔄 State** | SeatStatus (AVAILABLE, RESERVED, ฯลฯ) |

---

<p align="center">Made with ❤️ by T Olio</p>
