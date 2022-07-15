import bpy
import random
import os

from .render_operator import return_filepath

def generate_random():
    return(str(random.randrange(0,99999)).zfill(5))

def get_files_by_pattern(pattern, folder):
    file_list=[]
    for f in os.listdir(folder):
        if f.startswith(pattern):
            file_list.append(os.path.join(folder, f))
    return file_list

def delete_file(filepath) :
    try:
        if os.path.isfile(filepath) :
            os.remove(filepath)
            return True
    except PermissionError:
        return False

class PLAYBLASTER_OT_manage_actions(bpy.types.Operator):
    bl_idname = "playblaster.manage_actions"
    bl_label = "Manage Playblasts"

    action: bpy.props.EnumProperty(items=(
        ('UP', 'Up', ""),
        ('DOWN', 'Down', ""),
        ('ADD', 'Add', ""),
        ('REMOVE', 'Remove', ""),
        ))
    remove_files: bpy.props.BoolProperty(name="Remove associated playblasts")

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def invoke(self, context, event):
        if self.action=='REMOVE':
            self.remove_files=False
            return context.window_manager.invoke_props_dialog(self)
        return self.execute(context)
 
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "remove_files")

    def execute(self, context):
        scn=context.scene
        props = scn.playblaster_properties
        playblasts = props.playblasts
        check_indexes=False

        # Actions
        if self.action=="ADD":
            new_playblast=playblasts.add()
            new_playblast.name="New Playblast"
            new_playblast.frame_range_in=scn.frame_start
            new_playblast.frame_range_out=scn.frame_end
            new_playblast.hash=generate_random()
            props.playblast_index=new_playblast.index=len(playblasts)-1

        elif self.action=="REMOVE":
            if props.playblast_index<=len(playblasts)-1:
                check_indexes=True

                # remove associated
                if self.remove_files:
                    playblast=playblasts[props.playblast_index]
                    for f in get_files_by_pattern(playblast.hash, os.path.dirname(return_filepath(playblast))):
                        delete_file(f)

                playblasts.remove(props.playblast_index)
                if props.playblast_index>len(playblasts)-1:
                    props.playblast_index-=1
                elif len(playblasts)==0:
                    props.playblast_index=-1

        elif self.action in {"UP", "DOWN"}:
            if self.action=="UP":
                target = props.playblast_index-1
            else:
                target = props.playblast_index+1
            if target!=-1 and target<len(playblasts):
                check_indexes=True
                playblasts.move(props.playblast_index, target)
                props.playblast_index=target

        # Recalculate indexes
        if check_indexes:
            n=0
            for p in playblasts:
                p.index=n
                n+=1

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PLAYBLASTER_OT_manage_actions)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_manage_actions)