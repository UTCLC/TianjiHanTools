import os
import shutil
import json
import datetime
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
class ProjectManager(QObject):
    project_loaded = Signal(dict)  # 工程加载成功信号
    project_saved = Signal()       # 工程保存成功信号
    error_occurred = Signal(str)   # 错误发生信号

    def __init__(self):
        super().__init__()
        self.current_project = None

    def new_project(self, parent_window):
        """创建新工程"""
        src_folder = self._get_directory(parent_window, "选择源文件夹")
        if not src_folder: return

        project_folder = self._get_directory(parent_window, "选择工程文件夹")
        if not project_folder: return

        try:
            project_data = self._create_project_structure(src_folder, project_folder)
            self.current_project = project_data
            self.project_loaded.emit(project_data)
        except Exception as e:
            self.error_occurred.emit(f"创建工程失败：{str(e)}")

    def open_project(self, parent_window):
        """打开已有工程"""
        project_folder = self._get_directory(parent_window, "选择工程文件夹")
        if not project_folder: return

        project_file = os.path.join(project_folder, 'project.json')
        if not os.path.exists(project_file):
            self.error_occurred.emit("无效的工程目录")
            return

        try:
            with open(project_file, 'r') as f:
                project_data = json.load(f)
            project_data['project_path'] = project_folder  # 确保路径最新
            self._validate_project(project_data)
            
            self.current_project = project_data
            self.project_loaded.emit(project_data)
        except Exception as e:
            self.error_occurred.emit(f"加载工程失败：{str(e)}")

    def save_project(self):
        """保存当前工程"""
        if not self.current_project:
            self.error_occurred.emit("没有正在编辑的工程")
            return

        try:
            self.current_project['last_modified'] = datetime.datetime.now().isoformat()
            project_file = os.path.join(self.current_project['project_path'], 'project.json')
            
            with open(project_file, 'w') as f:
                json.dump(self.current_project, f, indent=4)
            
            self.project_saved.emit()
        except Exception as e:
            self.error_occurred.emit(f"保存失败：{str(e)}")

    def _create_project_structure(self, src_folder, project_folder):
        """创建工程目录结构"""
        source_dir = os.path.join(project_folder, 'source')
        target_dir = os.path.join(project_folder, 'target')
        
        # 清理已存在的目录
        for d in [source_dir, target_dir]:
            if os.path.exists(d):
                shutil.rmtree(d)
        
        # 复制文件
        shutil.copytree(src_folder, source_dir)
        shutil.copytree(src_folder, target_dir)

        # 生成工程数据
        return {
            'project_path': project_folder,
            'source': source_dir,
            'target': target_dir,
            'created_at': datetime.datetime.now().isoformat(),
            'last_modified': ''
        }

    def _get_directory(self, parent, title):
        """通用目录选择对话框"""
        return QFileDialog.getExistingDirectory(parent, title)

    def _validate_project(self, project_data):
        """验证工程有效性"""
        required_dirs = ['source', 'target']
        for d in required_dirs:
            if not os.path.isdir(os.path.join(project_data['project_path'], d)):
                raise ValueError(f"缺失必需目录: {d}")