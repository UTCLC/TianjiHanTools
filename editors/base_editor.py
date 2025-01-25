from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

class BaseEditor(QWidget):
    def __init__(self, source_path, target_path):
        super().__init__()
        self.source_path = source_path
        self.target_path = target_path
        self.modified = Signal(bool)
        self.init_ui()
        
    def init_ui(self):
        raise NotImplementedError("必须实现init_ui方法")
        
    def get_content(self):
        raise NotImplementedError("必须实现get_content方法")