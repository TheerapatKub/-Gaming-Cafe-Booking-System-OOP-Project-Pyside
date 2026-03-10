"""
Gaming Cafe Booking System - Main Entry Point
วิชาการเขียนโปรแกรมเชิงวัตถุ (OOP) - Final Team Project
Framework: PySide6 (Desktop GUI)
"""
import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
