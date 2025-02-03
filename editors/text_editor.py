from PySide6.QtWidgets import QHBoxLayout, QPlainTextEdit
from .base_editor import BaseEditor
import loc

class TextEditor(BaseEditor):
    def _handle_modify(self):
        self.modified.emit(True)

    def init_ui(self):
        layout = QHBoxLayout(self)
        
        self.source_editor = QPlainTextEdit()
        try:
            with open(self.source_path, 'r', encoding='utf-8') as f:
                self.source_editor.setPlainText(f.read())
        except:
            self.source_editor.setPlainText(loc.translate("locUnable2LoadSrcFile"))
        self.source_editor.setReadOnly(True)
        
        self.target_editor = QPlainTextEdit()
        try:
            with open(self.target_path, 'r', encoding='utf-8') as f:
                self.target_editor.setPlainText(f.read())
        except:
            self.target_editor.setPlainText("")
        
        layout.addWidget(self.source_editor)
        layout.addWidget(self.target_editor)

        self.target_editor.textChanged.connect(self._handle_modify)
        
    def get_content(self):
        return self.target_editor.toPlainText()