import json
from PySide6.QtWidgets import QHBoxLayout, QTableWidget, QTableWidgetItem
from .base_editor import BaseEditor
import loc

class JSONEditor(BaseEditor):
    def init_ui(self):
        layout = QHBoxLayout(self)
        self.table = QTableWidget()
        
        source_data = self._load_json(self.source_path)
        try:
            target_data = self._load_json(self.target_path)
        except:
            target_data = source_data.copy()
        
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([loc.translate("locKey"), loc.translate("locSrcTxt"), loc.translate("locTarTxt")])
        self.table.setRowCount(len(source_data))
        
        for row, (key, value) in enumerate(source_data.items()):
            self.table.setItem(row, 0, QTableWidgetItem(key))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))
            target_value = target_data.get(key, "")
            self.table.setItem(row, 2, QTableWidgetItem(str(target_value)))
        
        layout.addWidget(self.table)
        
    def get_content(self):
        data = {}
        for row in range(self.table.rowCount()):
            key_item = self.table.item(row, 0)
            value_item = self.table.item(row, 2)
            if key_item and value_item:
                data[key_item.text()] = value_item.text()
        return json.dumps(data, ensure_ascii=False, indent=4)
    
    def _load_json(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}