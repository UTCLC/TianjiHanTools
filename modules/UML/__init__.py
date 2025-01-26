import os
import shutil
from pythonnet import load
load("coreclr")
import clr
r_path = os.path.dirname(os.path.abspath(__file__))
clr.AddReference(r_path + r"\UndertaleModLib.dll")
import UndertaleModLib # type: ignore
import UndertaleModLib.Models as mod # type: ignore
from System.IO import FileInfo, FileStream, FileMode, FileAccess, FileShare # type: ignore

class GameMakerLib:
    def Read(filepath):
        stream = None
        try:
            stream = FileStream(filepath, FileMode.Open, FileAccess.Read)
            gmData = UndertaleModLib.UndertaleIO.Read(stream)
            return gmData
        finally:
            if stream is not None:
                stream.Close()

    def Write(filepath, Content):
        temp_path = filepath + "temp"
        stream = None
        try:
            stream = FileStream(temp_path, FileMode.Create, FileAccess.Write)
            UndertaleModLib.UndertaleIO.Write(stream, Content)
        finally:
            if stream is not None:
                stream.Close()
        shutil.move(temp_path, filepath)

    def String(str):
        return mod.UndertaleString(str)