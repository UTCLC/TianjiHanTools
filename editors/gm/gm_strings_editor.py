from PySide6.QtWidgets import QHBoxLayout, QPlainTextEdit, QVBoxLayout, QLabel
from .gm_base_editor import BaseEditor
from modules.UML import GameMakerLib as gml

class GMStringsEditor(BaseEditor):
    def _handle_modify(self):
        self.save()
        self.modified.emit(True)

    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # 源文本侧布局
        source_layout = QVBoxLayout()
        source_layout.addWidget(QLabel("源文本"))
        self.source_editor = QPlainTextEdit()
        try:
            self.source_editor.setPlainText(self.source_data.Strings[int(self.id)].Content)
        except:
            self.source_editor.setPlainText("无法读取源文本")
        self.source_editor.setReadOnly(True)
        source_layout.addWidget(self.source_editor)

        # 目标文本侧布局
        target_layout = QVBoxLayout()
        target_layout.addWidget(QLabel("目标文本"))
        self.target_editor = QPlainTextEdit()
        try:
            self.target_editor.setPlainText(self.target_data.Strings[int(self.id)].Content)
        except:
            self.target_editor.setPlainText("")
        target_layout.addWidget(self.target_editor)

        layout.addLayout(source_layout)
        layout.addLayout(target_layout)

        self.target_editor.textChanged.connect(self._handle_modify)
        
    def save(self):
        self.target_data.Strings[int(self.id)].Content = self.target_editor.toPlainText()