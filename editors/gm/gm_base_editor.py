from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

class GMBaseEditor(QWidget):
    modified = Signal(bool)
    def __init__(self, source_data, target_data, id):
        super().__init__()
        self.source_data = source_data
        self.target_data = target_data
        self.id = id
        self.init_ui()

    def init_ui(self):
        raise NotImplementedError("必须实现init_ui方法")
        
    def save(self):
        raise NotImplementedError("必须实现save方法")