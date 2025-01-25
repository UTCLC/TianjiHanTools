import os
from pythonnet import load
load("coreclr")
import clr
r_path = os.path.dirname(os.path.abspath(__file__))
clr.AddReference(r_path + r"\UndertaleModLib.dll")
import UndertaleModLib # type: ignore
from System.IO import FileInfo, FileStream, FileMode, FileAccess # type: ignore

class GameMakerLib:
    def Read(self,filepath):
        stream = FileStream(filepath, FileMode.Open, FileAccess.Read)
        gmData = UndertaleModLib.UndertaleIO.Read(stream)
        return gmData