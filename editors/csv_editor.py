import csv
from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHBoxLayout)
from .base_editor import BaseEditor
from PySide6.QtCore import Qt
from utils import detect_encoding
import loc

class CSVEditor(BaseEditor):
    def init_ui(self):
        layout = QHBoxLayout(self)
        self.table = QTableWidget()
        
        # 读取源文件和目标文件
        source_data = self._load_csv(self.source_path)
        try:
            target_data = self._load_csv(self.target_path)
        except:
            target_data = source_data.copy()

        # 合并数据并创建表格
        self._create_table(source_data, target_data)
        
        layout.addWidget(self.table)

    def get_content(self):
        return self._generate_csv_content()

    def _load_csv(self, file_path):
        try:
            with open(file_path, 'r', encoding=detect_encoding(file_path)) as f:
                return list(csv.reader(f))
        except Exception as e:
            print(f"Error loading CSV: {str(e)}")
            return []

    def _create_table(self, source_data, target_data):
        # 确保数据一致性
        row_count = max(len(source_data), len(target_data))
        col_count = max(
            len(source_data[0]) if source_data else 0,
            len(target_data[0]) if target_data else 0
        )

        self.table.setRowCount(row_count)
        self.table.setColumnCount(col_count * 2)  # 源文件列 + 目标文件列

        # 设置表头
        headers = []
        for i in range(col_count):
            headers.append(f"{loc.translate("locSourceColumn")} {i+1}")
            headers.append(f"{loc.translate("locTargetColumn")} {i+1}")
        self.table.setHorizontalHeaderLabels(headers)

        # 填充数据
        for row_idx in range(row_count):
            for col_idx in range(col_count):
                # 源数据单元格
                source_item = QTableWidgetItem()
                if row_idx < len(source_data) and col_idx < len(source_data[row_idx]):
                    source_item.setText(source_data[row_idx][col_idx])
                source_item.setFlags(source_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_idx, col_idx*2, source_item)

                # 目标数据单元格
                target_item = QTableWidgetItem()
                if row_idx < len(target_data) and col_idx < len(target_data[row_idx]):
                    target_item.setText(target_data[row_idx][col_idx])
                self.table.setItem(row_idx, col_idx*2 + 1, target_item)

    def _generate_csv_content(self):
        content = []
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(1, self.table.columnCount(), 2):  # 仅取目标列
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            content.append(row_data)
        
        # 转换为CSV格式
        output = []
        try:
            with open(self.target_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(content)
        except Exception as e:
            print(f"Error saving CSV: {str(e)}")
        return content