import os
from chardet import detect

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        return detect(f.read())['encoding']

def get_relative_path(full_path, base_path):
    return os.path.relpath(full_path, base_path)