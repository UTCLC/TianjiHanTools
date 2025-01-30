class ToolsRegister():
    def ToolTxTFormatLate(self, parent):
        from tools.txt_format_late import ToolTxTFormatLate
        parent.tool_window = ToolTxTFormatLate()
        parent.tool_window.show()