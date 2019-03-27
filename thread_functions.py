import bpy , subprocess, threading, os, platform

from .preferences import get_addon_preferences
from .misc_functions import absolute_path, create_dir, delete_file, get_file_in_folder

# render function
def render_function(cmd, total_frame, scene, folder_path, output_name, blend_file) :
    # launch rendering
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    frame_count = 0
    while True :
        line = process.stdout.readline()
        if line != '' :
            if b"Append frame " in line :
                frame_count += 1
                scene.playblaster_completion = frame_count / total_frame * 100
            if b"Blender quit" in line :
                break
        else:
            break

    #open video
    filepath = get_file_in_folder(folder_path, output_name)
    if filepath != "" :
        open_video_file(filepath)

    #delete blend file
    delete_file(blend_file)

# launch threading
def threading_render(arguments) :
    render_thread = threading.Thread(target=render_function, args=arguments)
    render_thread.start()

def open_video_file(file_path) :
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', file_path))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(file_path)
    else:                                   # linux variants
        subprocess.call(('xdg-open', file_path))
