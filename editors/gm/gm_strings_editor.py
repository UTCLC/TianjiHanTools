from PySide6.QtWidgets import QHBoxLayout, QPlainTextEdit
from .gm_base_editor import BaseEditor
from modules.UML import GameMakerLib as gml

class GMStringsEditor(BaseEditor):
    def _handle_modify(self):
        self.save()
        self.modified.emit(True)

    def init_ui(self):
        layout = QHBoxLayout(self)
        
        self.source_editor = QPlainTextEdit()
        try:
            self.source_editor.setPlainText(self.source_data.Strings[int(self.id)].Content)
        except:
            self.source_editor.setPlainText("无法读取源文件")
        self.source_editor.setReadOnly(True)
        
        self.target_editor = QPlainTextEdit()
        try:
            self.target_editor.setPlainText(self.target_data.Strings[int(self.id)].Content)
        except:
            self.target_editor.setPlainText("")
        
        layout.addWidget(self.source_editor)
        layout.addWidget(self.target_editor)

        self.target_editor.textChanged.connect(self._handle_modify)
        
    def save(self):
        self.target_data.Strings[int(self.id)].Content = self.target_editor.toPlainText()