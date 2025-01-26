from PySide6.QtWidgets import QDockWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt, Signal
import os

class FileExplorer(QDockWidget):
    file_double_clicked = Signal(str)  # 发送相对路径
    
    def __init__(self, parent=None):
        super().__init__("文件浏览器", parent)
        self.data = [{},{}]
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("项目文件")
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.setWidget(self.tree)

    def on_item_double_clicked(self, item):
        if not item.childCount():
            rel_path = item.data(0, Qt.ItemDataRole.UserRole)
            if rel_path:
                self.file_double_clicked.emit(rel_path)

    def load_project(self, project_data):
        self.tree.clear()
        if not project_data:
            return

        source_dir = project_data['source']
        self._populate_tree(self.tree, source_dir, project_data)

    def _populate_tree(self, parent, path, base_data):
        for item_name in sorted(os.listdir(path)):
            item_path = os.path.join(path, item_name)
            node = QTreeWidgetItem(parent)
            node.setText(0, item_name)
            if os.path.isdir(item_path):
                self._populate_tree(node, item_path, base_data)
            elif item_name.endswith('.win'):
                self._populate_tree_gm(node, item_path, base_data)
            else:
                rel_path = os.path.relpath(item_path, base_data['source'])
                node.setData(0, Qt.ItemDataRole.UserRole, f"file:{rel_path}")

    def _populate_tree_gm(self, parent, path, base_data):
        from modules.UML import GameMakerLib as gml
        rel_path = os.path.relpath(path, base_data['source'])
        self.data[0][rel_path] = gml.Read(base_data['source'] + "/" + rel_path)
        self.data[1][rel_path] = gml.Read(base_data['target'] + "/" + rel_path)
        pnode = QTreeWidgetItem(parent)
        pnode.setText(0, "Strings")
        for i in range(len(self.data[0][rel_path].Strings)):
            node = QTreeWidgetItem(pnode)
            node.setText(0, str(self.data[0][rel_path].Strings[i]))
            node.setData(0, Qt.ItemDataRole.UserRole, f"gm:{rel_path}/GMStrings/{i}")
            

    def show_or_close(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()