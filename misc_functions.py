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