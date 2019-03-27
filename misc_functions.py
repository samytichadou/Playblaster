import bpy
import os
import signal

# absolute path
def absolute_path(path) :
    apath = os.path.abspath(bpy.path.abspath(path))
    return apath

# create directory if doesn't exist
def create_dir(dir_path) :
    if os.path.isdir(dir_path) == False :
            os.makedirs(dir_path)

#kill subprocess
def kill_subprocess(process):
    if process !='':
        os.kill(int(process), signal.SIGTERM)

#delete filepath
def delete_file(filepath) :
    if os.path.isfile(filepath) :
        os.remove(filepath)

#get file in folder with pattern :
def get_file_in_folder(folder, pattern) :
    file_path = ""
    for file in os.listdir(folder) :
        if pattern in file :
            file_path = os.path.join(folder, file)
    return file_path
