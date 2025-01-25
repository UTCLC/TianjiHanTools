import sys
from PySide6.QtWidgets import QApplication
from main_window import LocalizationIDE

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("windowsvista")
    window = LocalizationIDE()
    window.show()
    sys.exit(app.exec())