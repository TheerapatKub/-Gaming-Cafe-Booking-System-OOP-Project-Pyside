"""
Main Window - CAFE. e-Sports Booking (แปลงจาก React ตัวใหม่)
เชื่อมกับ SeatRepository, BookingService
"""
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QStackedWidget, QScrollArea,
    QFrame, QGridLayout, QButtonGroup, QSpinBox, QDateEdit, QTimeEdit,
    QMessageBox,
)
from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtGui import QPainter, QPen, QColor

from ..models.seat import Seat
from ..models.user import Customer
from ..services.booking_service import BookingService
from ..repositories.seat_repository import SeatRepository

ZONES = [
    {"id": "standard", "title": "Standard", "price": 40, "desc": "จอ 144Hz / การ์ดจอ RTX 3060", "seat_type": "StandardSeat"},
    {"id": "premium", "title": "Premium", "price": 80, "desc": "จอ 240Hz / การ์ดจอ RTX 4070", "seat_type": "PremiumSeat"},
    {"id": "privateroom", "title": "Private Room", "price": 250, "desc": "ห้องส่วนตัว / จอคู่ 360Hz", "seat_type": "PrivateRoomSeat"},
]

STYLE_SHEET = """
QWidget { font-family: "Segoe UI", "Kanit", sans-serif; color: #111827; background-color: #ffffff; }
QScrollArea { border: none; background-color: #ffffff; }
QScrollBar:vertical { border: none; background: #f3f4f6; width: 10px; }
QScrollBar::handle:vertical { background: #d1d5db; min-height: 20px; border-radius: 5px; }

QLineEdit, QSpinBox, QDateEdit, QTimeEdit {
    background-color: #f9fafb; border: 2px solid transparent; border-radius: 16px;
    padding: 14px 18px; font-size: 16px;
}
QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QTimeEdit:focus {
    border: 2px solid #000000; background-color: #ffffff;
}

QPushButton.toggle-btn {
    background-color: #f9fafb; border: 2px solid transparent; border-radius: 16px;
    padding: 14px; font-size: 16px; font-weight: bold; color: #4b5563;
}
QPushButton.toggle-btn:checked { background-color: #000000; color: #ffffff; }

QPushButton.zone-card {
    background-color: #ffffff; border: 2px solid #f3f4f6; border-radius: 32px;
    padding: 20px; text-align: left;
}
QPushButton.zone-card:hover { border-color: #d1d5db; background-color: #f9fafb; }
QPushButton.zone-card:checked { border: 2px solid #000000; background-color: #ffffff; }

QFrame.seat-panel {
    background-color: #f9fafb; border: 1px solid #f3f4f6; border-radius: 32px;
}

QPushButton.seat-btn {
    background-color: #ffffff; border: 2px solid #e5e7eb; border-radius: 16px;
    font-size: 14px; font-weight: bold; color: #4b5563;
}
QPushButton.seat-btn:hover:!disabled { border-color: #000000; color: #000000; }
QPushButton.seat-btn:checked { background-color: #000000; border-color: #000000; color: #ffffff; }
QPushButton.seat-btn:disabled { background-color: #f3f4f6; border-color: #e5e7eb; color: #d1d5db; }

QFrame.summary-panel { background-color: #f9fafb; border-radius: 32px; }
QPushButton.action-btn {
    background-color: #000000; color: white; border-radius: 16px;
    padding: 18px; font-size: 18px; font-weight: bold;
}
QPushButton.action-btn:hover:!disabled { background-color: #1f2937; }
QPushButton.action-btn:disabled { background-color: #e5e7eb; color: #9ca3af; }

QFrame.qr-box { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 32px; }
QFrame.qr-header { background-color: #113566; border-top-left-radius: 32px; border-top-right-radius: 32px; }
"""


class SeatButton(QPushButton):
    def __init__(self, seat: Seat, parent=None):
        num = seat.seat_id[1:] if len(seat.seat_id) >= 2 and seat.seat_id[1:].isdigit() else seat.seat_id
        super().__init__(f"💻\n{num}", parent)
        self.seat = seat
        self.setCheckable(True)
        self.setProperty("class", "seat-btn")
        self.setFixedSize(64, 64)
        if not seat.is_available:
            self.setDisabled(True)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.seat.is_available:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(QColor("#d1d5db"), 2))
            painter.drawLine(0, 0, self.width(), self.height())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.booking_service = BookingService()
        self.setWindowTitle("Gaming Cafe - จองเครื่อง")
        self.setMinimumSize(1100, 800)
        self.setStyleSheet(STYLE_SHEET)

        self.step = 1
        self.booking_history = []

        self.state = {
            "type": "now",
            "date": QDate.currentDate(),
            "time": QTime.currentTime(),
            "duration": 3,
            "zone": None,
            "seat": None,
            "name": "",
            "phone": "",
            "paymentMethod": "qrcode",
        }

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self._init_page_1_form()
        self._init_page_2_qrcode()
        self._init_page_3_success()
        self._init_page_4_history()

        self.stacked_widget.addWidget(self.page_1)
        self.stacked_widget.addWidget(self.page_2)
        self.stacked_widget.addWidget(self.page_3)
        self.stacked_widget.addWidget(self.page_4)

        self._update_summary()

    def _go_step(self, n: int):
        self.step = n
        self.stacked_widget.setCurrentIndex(n - 1)
        if n == 4:
            self._refresh_history()

    def _init_page_1_form(self):
        self.page_1 = QWidget()
        main_layout = QVBoxLayout(self.page_1)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header = QHBoxLayout()
        header.setContentsMargins(24, 24, 24, 0)
        logo = QLabel("Gaming Cafe")
        logo.setStyleSheet("font-size: 24px; font-weight: 900; color: #111827;")
        logo.setCursor(Qt.CursorShape.PointingHandCursor)
        logo.mousePressEvent = lambda e: self._reset_booking()
        header.addWidget(logo)
        header.addStretch()
        self.btn_history = QPushButton("📋 ประวัติการจอง")
        self.btn_history.setStyleSheet("background: #f9fafb; color: #6b7280; font-weight: bold; border-radius: 999px; padding: 8px 16px;")
        self.btn_history.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_history.clicked.connect(lambda: self._go_step(4))
        header.addWidget(self.btn_history)
        self.history_badge = QLabel("")
        self.history_badge.setStyleSheet("background: black; color: white; font-size: 10px; padding: 2px 6px; border-radius: 999px;")
        self.history_badge.setVisible(False)
        header.addWidget(self.history_badge)
        main_layout.addLayout(header)

        content = QHBoxLayout()
        content.setContentsMargins(40, 24, 40, 40)
        content.setSpacing(48)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(32)

        form_layout.addWidget(QLabel("จองที่นั่ง"))
        form_layout.addWidget(QLabel("เลือกเวลาและโซนที่ต้องการ"))

        sec1 = QVBoxLayout()
        sec1.setSpacing(16)
        sec1.addWidget(QLabel("1. เวลาเข้าใช้งาน"))

        type_row = QHBoxLayout()
        self.type_group = QButtonGroup(self)
        self.btn_now = QPushButton("จองตอนนี้")
        self.btn_adv = QPushButton("จองล่วงหน้า")
        for btn in (self.btn_now, self.btn_adv):
            btn.setCheckable(True)
            btn.setProperty("class", "toggle-btn")
            btn.setFixedHeight(56)
            self.type_group.addButton(btn)
            type_row.addWidget(btn)
        self.btn_now.setChecked(True)
        self.type_group.buttonClicked.connect(self._on_type_changed)
        sec1.addLayout(type_row)

        self.datetime_widget = QWidget()
        dt_layout = QHBoxLayout(self.datetime_widget)
        dt_layout.setSpacing(16)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(self.state["date"])
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.dateChanged.connect(lambda d: self._update_state("date", d))
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(self.state["time"])
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.timeChanged.connect(lambda t: self._update_state("time", t))
        dt_layout.addWidget(QLabel("วันที่"))
        dt_layout.addWidget(self.date_edit)
        dt_layout.addWidget(QLabel("เวลา"))
        dt_layout.addWidget(self.time_edit)
        self.datetime_widget.setVisible(False)
        sec1.addWidget(self.datetime_widget)

        dur_box = QVBoxLayout()
        dur_box.addWidget(QLabel("จำนวนชั่วโมง"))
        dur_row = QHBoxLayout()
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 24)
        self.spin_duration.setValue(3)
        self.spin_duration.setFixedHeight(56)
        self.spin_duration.valueChanged.connect(lambda v: self._update_state("duration", v))
        dur_row.addWidget(self.spin_duration)
        dur_row.addWidget(QLabel("ชั่วโมง"))
        dur_row.addStretch()
        dur_box.addLayout(dur_row)
        sec1.addLayout(dur_box)
        form_layout.addLayout(sec1)

        sec2 = QVBoxLayout()
        sec2.setSpacing(16)
        sec2.addWidget(QLabel("2. โซนและที่นั่ง"))

        self.zone_group = QButtonGroup(self)
        for z in ZONES:
            btn = QPushButton(f"{z['title']}\n{z['desc']}\n{z['price']}฿/ชม.")
            btn.setCheckable(True)
            btn.setProperty("class", "zone-card")
            btn.setProperty("zone_id", z["id"])
            self.zone_group.addButton(btn)
            sec2.addWidget(btn)

        self.seat_panel = QFrame()
        self.seat_panel.setProperty("class", "seat-panel")
        sp_layout = QVBoxLayout(self.seat_panel)
        sp_layout.setContentsMargins(24, 24, 24, 24)
        self.zone_header = QHBoxLayout()
        self.zone_header.addWidget(QLabel("💻"))
        self.lbl_zone_name = QLabel("")
        self.lbl_zone_name.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.zone_header.addWidget(self.lbl_zone_name)
        self.zone_header.addStretch()
        self.lbl_zone_price = QLabel("")
        self.lbl_zone_price.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 999px; padding: 4px 12px; font-size: 12px;")
        self.zone_header.addWidget(self.lbl_zone_price)
        sp_layout.addLayout(self.zone_header)
        self.seat_grid = QGridLayout()
        sp_layout.addLayout(self.seat_grid)
        self.seat_panel.setVisible(False)
        self.seat_group = QButtonGroup(self)
        self.seat_group.buttonClicked.connect(self._on_seat_changed)
        sec2.addWidget(self.seat_panel)
        form_layout.addLayout(sec2)

        sec3 = QVBoxLayout()
        sec3.setSpacing(16)
        sec3.addWidget(QLabel("3. ข้อมูลของคุณ"))
        self.inp_name = QLineEdit()
        self.inp_name.setPlaceholderText("ชื่อ - นามสกุล")
        self.inp_name.setFixedHeight(56)
        self.inp_name.textChanged.connect(lambda t: self._update_state("name", t))
        self.inp_phone = QLineEdit()
        self.inp_phone.setPlaceholderText("เบอร์โทรศัพท์")
        self.inp_phone.setFixedHeight(56)
        self.inp_phone.textChanged.connect(lambda t: self._update_state("phone", t))
        info_row = QHBoxLayout()
        info_row.addWidget(self.inp_name)
        info_row.addWidget(self.inp_phone)
        sec3.addLayout(info_row)
        form_layout.addLayout(sec3)

        scroll.setWidget(form_widget)
        content.addWidget(scroll, stretch=7)

        summary = QFrame()
        summary.setProperty("class", "summary-panel")
        summary.setFixedWidth(360)
        sum_layout = QVBoxLayout(summary)
        sum_layout.setContentsMargins(32, 32, 32, 32)
        sum_layout.setSpacing(20)
        sum_layout.addWidget(QLabel("สรุปการจอง"))

        self.lbl_sum_type = QLabel("จองตอนนี้")
        self.lbl_sum_zone = QLabel("-")
        self.lbl_sum_seat = QLabel("ยังไม่ได้เลือก")
        self.lbl_sum_date = QLabel("-")
        self.lbl_sum_time = QLabel("-")
        self.lbl_sum_duration = QLabel("3 ชม.")
        sum_layout.addLayout(self._row("ประเภทการจอง", self.lbl_sum_type))
        sum_layout.addLayout(self._row("โซนที่นั่ง", self.lbl_sum_zone))
        sum_layout.addLayout(self._row("หมายเลขเครื่อง", self.lbl_sum_seat))
        self.datetime_summary = QWidget()
        dt_sum_layout = QVBoxLayout(self.datetime_summary)
        dt_sum_layout.setContentsMargins(0, 0, 0, 0)
        dt_sum_layout.addLayout(self._row("วันที่", self.lbl_sum_date))
        dt_sum_layout.addLayout(self._row("เวลา", self.lbl_sum_time))
        self.datetime_summary.setVisible(False)
        sum_layout.addWidget(self.datetime_summary)
        sum_layout.addLayout(self._row("ระยะเวลา", self.lbl_sum_duration))

        sum_layout.addSpacing(16)
        sum_layout.addWidget(QLabel("ช่องทางการชำระเงิน"))
        pay_row = QHBoxLayout()
        self.btn_qr = QPushButton("📱 สแกนจ่าย")
        self.btn_qr.setCheckable(True)
        self.btn_qr.setChecked(True)
        self.btn_qr.setProperty("class", "toggle-btn")
        self.btn_cash = QPushButton("👤 จ่ายที่ร้าน")
        self.btn_cash.setCheckable(True)
        self.btn_cash.setProperty("class", "toggle-btn")
        pay_row.addWidget(self.btn_qr)
        pay_row.addWidget(self.btn_cash)
        self.pay_group = QButtonGroup(self)
        self.pay_group.addButton(self.btn_qr)
        self.pay_group.addButton(self.btn_cash)
        self.pay_group.buttonClicked.connect(self._on_payment_changed)
        sum_layout.addLayout(pay_row)

        sum_layout.addSpacing(24)
        total_row = QHBoxLayout()
        total_row.addWidget(QLabel("ยอดรวมทั้งสิ้น"))
        total_row.addStretch()
        self.lbl_total = QLabel("0 ฿")
        self.lbl_total.setStyleSheet("font-size: 36px; font-weight: 900;")
        total_row.addWidget(self.lbl_total)
        sum_layout.addLayout(total_row)

        sum_layout.addStretch()
        self.btn_submit = QPushButton("ดำเนินการชำระเงิน")
        self.btn_submit.setProperty("class", "action-btn")
        self.btn_submit.clicked.connect(self._on_submit)
        sum_layout.addWidget(self.btn_submit)
        self.lbl_hint = QLabel("กรุณากรอกข้อมูลและเลือกเครื่องให้ครบถ้วน")
        self.lbl_hint.setStyleSheet("font-size: 13px; color: #6b7280;")
        self.lbl_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sum_layout.addWidget(self.lbl_hint)

        content.addWidget(summary, stretch=5)
        main_layout.addLayout(content)

        self.zone_group.buttonClicked.connect(self._on_zone_changed)

    def _init_page_2_qrcode(self):
        self.page_2 = QWidget()
        layout = QVBoxLayout(self.page_2)
        layout.setContentsMargins(40, 40, 40, 40)

        btn_back = QPushButton("← ย้อนกลับ")
        btn_back.setStyleSheet("border: none; color: #6b7280; font-weight: bold; font-size: 16px;")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(lambda: self._go_step(1))
        layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

        qr_box = QFrame()
        qr_box.setProperty("class", "qr-box")
        qr_box.setFixedSize(420, 520)
        qr_layout = QVBoxLayout(qr_box)
        qr_layout.setContentsMargins(0, 0, 0, 0)

        qr_header = QFrame()
        qr_header.setProperty("class", "qr-header")
        qr_header.setFixedHeight(100)
        h_layout = QVBoxLayout(qr_header)
        h_layout.addWidget(QLabel("สแกนเพื่อชำระเงิน"), alignment=Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(QLabel("PromptPay / Mobile Banking"), alignment=Qt.AlignmentFlag.AlignCenter)
        qr_layout.addWidget(qr_header)

        body = QVBoxLayout()
        body.setContentsMargins(32, 32, 32, 32)
        qr_placeholder = QLabel("พื้นที่แสดง QR Code")
        qr_placeholder.setFixedSize(224, 224)
        qr_placeholder.setStyleSheet("background: #f9fafb; border: 2px dashed #d1d5db; border-radius: 24px; color: #9ca3af; font-size: 14px;")
        qr_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.addWidget(qr_placeholder, alignment=Qt.AlignmentFlag.AlignCenter)
        body.addWidget(QLabel("ยอดชำระสุทธิ"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.lbl_qr_price = QLabel("0 ฿")
        self.lbl_qr_price.setStyleSheet("font-size: 48px; font-weight: 900; color: #113566;")
        body.addWidget(self.lbl_qr_price, alignment=Qt.AlignmentFlag.AlignCenter)
        body.addStretch()
        btn_confirm = QPushButton("ยืนยันการโอนเงิน")
        btn_confirm.setProperty("class", "action-btn")
        btn_confirm.clicked.connect(self._on_confirm_transfer)
        body.addWidget(btn_confirm)
        body.addWidget(QLabel("เมื่อโอนเงินแล้ว กดเพื่อยืนยันและอัปโหลดสลิป"), alignment=Qt.AlignmentFlag.AlignCenter)
        qr_layout.addLayout(body)
        layout.addWidget(qr_box, alignment=Qt.AlignmentFlag.AlignCenter)

    def _init_page_3_success(self):
        self.page_3 = QWidget()
        layout = QVBoxLayout(self.page_3)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("✅")
        icon.setStyleSheet("font-size: 64px;")
        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("จองสำเร็จ!"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.lbl_success_desc = QLabel("")
        layout.addWidget(self.lbl_success_desc, alignment=Qt.AlignmentFlag.AlignCenter)

        receipt = QFrame()
        receipt.setFixedWidth(450)
        receipt.setStyleSheet("background: #f9fafb; border-radius: 24px; padding: 24px;")
        r_layout = QVBoxLayout(receipt)
        self.r_id = QLabel("-")
        self.r_type = QLabel("-")
        self.r_zone = QLabel("-")
        self.r_datetime = QLabel("-")
        self.r_duration = QLabel("-")
        self.r_status = QLabel("-")
        for lbl in [self.r_id, self.r_type, self.r_zone, self.r_datetime, self.r_duration, self.r_status]:
            lbl.setStyleSheet("font-weight: bold;")
        r_layout.addLayout(self._row("รหัสการจอง", self.r_id))
        r_layout.addLayout(self._row("ประเภทการจอง", self.r_type))
        r_layout.addLayout(self._row("โซนที่นั่ง", self.r_zone))
        r_layout.addLayout(self._row("เข้าใช้งาน", self.r_datetime))
        r_layout.addLayout(self._row("ระยะเวลา", self.r_duration))
        r_layout.addLayout(self._row("สถานะการชำระเงิน", self.r_status))

        layout.addWidget(receipt, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_home = QPushButton("จองที่นั่งเพิ่ม หรือ กลับหน้าหลัก")
        btn_home.setStyleSheet("color: #6b7280; font-weight: 600; background: transparent; border: none; text-decoration: underline;")
        btn_home.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_home.clicked.connect(self._reset_booking)
        layout.addWidget(btn_home, alignment=Qt.AlignmentFlag.AlignCenter)

    def _init_page_4_history(self):
        self.page_4 = QWidget()
        layout = QVBoxLayout(self.page_4)
        layout.setContentsMargins(40, 40, 40, 40)

        header = QHBoxLayout()
        header.addWidget(QLabel("ประวัติการจอง"))
        header.addStretch()
        btn_back = QPushButton("← กลับหน้าหลัก")
        btn_back.setStyleSheet("color: #6b7280; font-weight: bold;")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(lambda: self._go_step(1))
        header.addWidget(btn_back)
        layout.addLayout(header)

        self.history_list = QWidget()
        self.history_layout = QVBoxLayout(self.history_list)
        layout.addWidget(self.history_list)

    def _row(self, label: str, value: QLabel):
        r = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #6b7280;")
        r.addWidget(lbl)
        r.addStretch()
        r.addWidget(value)
        return r

    def _update_state(self, key: str, value):
        self.state[key] = value
        self._update_summary()

    def _on_type_changed(self, btn):
        self.state["type"] = "now" if btn == self.btn_now else "advance"
        self.btn_now.setChecked(btn == self.btn_now)
        self.btn_adv.setChecked(btn == self.btn_adv)
        self.datetime_widget.setVisible(btn == self.btn_adv)
        self.datetime_summary.setVisible(btn == self.btn_adv)
        self._update_summary()

    def _on_payment_changed(self, btn):
        self.state["paymentMethod"] = "qrcode" if btn == self.btn_qr else "counter"
        self._update_summary()

    def _on_zone_changed(self, btn):
        zone_id = btn.property("zone_id")
        zone = next((z for z in ZONES if z["id"] == zone_id), None)
        if not zone or (self.state["zone"] and self.state["zone"]["id"] == zone["id"]):
            return
        self.state["zone"] = zone
        self.state["seat"] = None
        self.lbl_zone_name.setText(f"{zone['title']} ZONE")
        self.lbl_zone_price.setText(f"{zone['price']} ฿/ชม.")
        self.seat_panel.setVisible(True)

        for i in reversed(range(self.seat_grid.count())):
            w = self.seat_grid.itemAt(i).widget()
            if w:
                w.setParent(None)
        for b in self.seat_group.buttons():
            self.seat_group.removeButton(b)

        seats = [s for s in SeatRepository.get_all() if s.__class__.__name__ == zone["seat_type"]]
        for i, seat in enumerate(seats):
            btn = SeatButton(seat)
            self.seat_group.addButton(btn)
            self.seat_grid.addWidget(btn, i // 8, i % 8)
        self._update_summary()

    def _on_seat_changed(self, btn: SeatButton):
        self.state["seat"] = btn.seat
        self._update_summary()

    def _update_summary(self):
        s = self.state
        self.lbl_sum_type.setText("จองตอนนี้" if s["type"] == "now" else "จองล่วงหน้า")
        self.lbl_sum_zone.setText(s["zone"]["title"] if s["zone"] else "-")
        self.lbl_sum_seat.setText(f"เครื่อง {s['seat'].seat_id}" if s["seat"] else "ยังไม่ได้เลือก")
        self.lbl_sum_date.setText(s["date"].toString("dd/MM/yyyy") if s["type"] == "advance" else "-")
        self.lbl_sum_time.setText(f"{s['time'].toString('HH:mm')} น." if s["type"] == "advance" else "-")
        self.lbl_sum_duration.setText(f"{s['duration']} ชม.")

        # แสดงราคาทันทีเมื่อเลือกโซน + เครื่อง + ชั่วโมง (ไม่ต้องรอกรอกชื่อ/เบอร์)
        price = 0
        if s["zone"] and s["seat"] and s["duration"]:
            try:
                tmp_user = Customer("ลูกค้า", "0000000000", "C000")
                price = self.booking_service.calculate_price(s["seat"], s["duration"], tmp_user)
            except ValueError:
                price = 0
        self.lbl_total.setText(f"{int(price)} ฿")
        self.lbl_qr_price.setText(f"{int(price)} ฿")

        is_valid = bool(s["zone"] and s["seat"] and s["name"].strip() and s["phone"].strip() and
                        (s["type"] == "now" or (s["date"] and s["time"])))
        self.btn_submit.setEnabled(is_valid)

        if s["paymentMethod"] == "qrcode":
            self.btn_submit.setText("ดำเนินการชำระเงิน")
        else:
            self.btn_submit.setText("ยืนยันการจอง")

        if self.booking_history:
            self.history_badge.setText(str(len(self.booking_history)))
            self.history_badge.setVisible(True)
        else:
            self.history_badge.setVisible(False)

    def _on_submit(self):
        s = self.state
        if s["paymentMethod"] == "qrcode":
            self._go_step(2)
        else:
            self._finalize_booking("counter")

    def _on_confirm_transfer(self):
        self._finalize_booking("qrcode")

    def _finalize_booking(self, method: str):
        s = self.state
        name = s["name"].strip()
        phone = s["phone"].strip()
        try:
            user = Customer(name, phone, "C001")
            booking = self.booking_service.create_booking(user, s["seat"], s["duration"])
        except ValueError as e:
            QMessageBox.warning(self, "เกิดข้อผิดพลาด", str(e))
            return

        bid = booking.booking_id
        total = int(booking.total_price)
        status = "ชำระเงินแล้ว" if method == "qrcode" else "รอชำระที่ร้าน"

        self.r_id.setText(f"GC-{bid[1:] if bid.startswith('B') else bid}")
        self.r_type.setText("จองตอนนี้" if s["type"] == "now" else "จองล่วงหน้า")
        self.r_zone.setText(f"{s['zone']['title']} (เครื่อง {s['seat'].seat_id})")
        if s["type"] == "advance":
            self.r_datetime.setText(f"{s['date'].toString('dd/MM/yyyy')} เวลา {s['time'].toString('HH:mm')} น.")
        else:
            self.r_datetime.setText("ใช้งานทันที")
        self.r_duration.setText(f"{s['duration']} ชม.")
        self.r_status.setText(status)
        self.r_status.setStyleSheet("font-weight: bold; color: #16a34a;" if method == "qrcode" else "font-weight: bold; color: #f97316;")
        self.lbl_success_desc.setText(f'แจ้งชื่อ "{name}" ที่หน้าเคาน์เตอร์\nเพื่อเข้าใช้งานได้เลยครับ')

        self.booking_history.insert(0, {
            "id": bid, "zone": s["zone"], "seat": s["seat"].seat_id, "duration": s["duration"],
            "name": name, "type": s["type"], "date": s["date"], "time": s["time"],
            "paymentMethod": s["paymentMethod"], "status": status, "total": total,
            "createdAt": datetime.now().strftime("%d/%m/%Y %H:%M"),
        })

        self._go_step(3)

    def _refresh_history(self):
        while self.history_layout.count():
            w = self.history_layout.takeAt(0).widget()
            if w:
                w.setParent(None)

        if not self.booking_history:
            empty = QFrame()
            empty.setStyleSheet("background: #f9fafb; border: 2px dashed #e5e7eb; border-radius: 32px;")
            empty.setMinimumHeight(200)
            layout = QVBoxLayout(empty)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(QLabel("📋"))
            layout.addWidget(QLabel("ยังไม่มีประวัติการจอง"))
            layout.addWidget(QLabel("เมื่อคุณทำการจองสำเร็จ ข้อมูลจะแสดงที่นี่"))
            self.history_layout.addWidget(empty)
        else:
            for h in self.booking_history:
                card = QFrame()
                card.setStyleSheet("background: white; border: 1px solid #e5e7eb; border-radius: 32px; padding: 24px;")
                card_layout = QVBoxLayout(card)
                row1 = QHBoxLayout()
                row1.addWidget(QLabel(f"GC-{str(h['id'])[1:] if str(h['id']).startswith('B') else h['id']}"))
                badge = QLabel(h["status"])
                badge.setStyleSheet("background: #dcfce7; color: #16a34a; padding: 4px 12px; border-radius: 999px; font-size: 12px;" if h["paymentMethod"] == "qrcode" else "background: #ffedd5; color: #f97316; padding: 4px 12px; border-radius: 999px; font-size: 12px;")
                row1.addWidget(badge)
                row1.addStretch()
                card_layout.addLayout(row1)
                card_layout.addWidget(QLabel(f"{h['zone']['title']} (เครื่อง {h['seat']}) • {h['duration']} ชม."))
                card_layout.addWidget(QLabel(f"ทำรายการเมื่อ: {h['createdAt']} | จองในชื่อ: {h['name']}"))
                row2 = QHBoxLayout()
                row2.addStretch()
                row2.addWidget(QLabel(f"{h['total']} ฿"))
                card_layout.addLayout(row2)
                self.history_layout.addWidget(card)

    def _reset_booking(self):
        self.state = {
            "type": "now", "date": QDate.currentDate(), "time": QTime.currentTime(),
            "duration": 3, "zone": None, "seat": None, "name": "", "phone": "", "paymentMethod": "qrcode",
        }
        self.btn_now.setChecked(True)
        self._on_type_changed(self.btn_now)
        self.date_edit.setDate(self.state["date"])
        self.time_edit.setTime(self.state["time"])
        self.spin_duration.setValue(3)
        self.zone_group.setExclusive(False)
        for btn in self.zone_group.buttons():
            btn.setChecked(False)
        self.zone_group.setExclusive(True)
        self.seat_panel.setVisible(False)
        self.inp_name.clear()
        self.inp_phone.clear()
        self.btn_qr.setChecked(True)
        self._update_summary()
        self._go_step(1)
