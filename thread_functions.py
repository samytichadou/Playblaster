import bpy , subprocess, threading

from .addon_preferences import get_addon_preferences
from .misc_functions import absolute_path, create_dir, delete_file, get_file_in_folder, find_os

# render function
def render_function(cmd, total_frame, scene, folder_path, output_name, blend_file) :
    scn = bpy.context.scene
    pb_props = scn.playblaster_properties

    debug = pb_props.debug
    # launch rendering
    if debug : print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    frame_count = 0
    while True :
        if not pb_props.is_rendering :
            if find_os() == 'win':
                subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=process.pid))
            else:
                process.kill()
            break
        line = process.stdout.readline()
        if line != '' :
            #debug
            if debug : print(line)
            if b"Append frame " in line :
                frame_count += 1
                try :
                    pb_props.completion = int(frame_count / total_frame * 100)
                except AttributeError :
                    #debug
                    if debug : print("AttributeError avoided")
                    pass

            if b"Blender quit" in line :
                break
        else:
            break

# launch threading
def threading_render(arguments) :
    render_thread = threading.Thread(target=render_function, args=arguments)
    render_thread.start()
