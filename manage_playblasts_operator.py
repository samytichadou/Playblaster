import bpy


class PLAYBLASTER_OT_manage_actions(bpy.types.Operator):
    bl_idname = "playblaster.manage_actions"
    bl_label = "Manage Playblasts"

    action : bpy.props.EnumProperty(items=(
        ('UP', 'Up', ""),
        ('DOWN', 'Down', ""),
        ('ADD', 'Add', ""),
        ('REMOVE', 'Remove', ""),
        ))

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = context.scene.playblaster_properties
        playblasts = props.playblasts

        if self.action=="ADD":
            new_action=playblasts.add()
            new_action.name="New Action"
            props.playblast_index=len(playblasts)-1

        elif self.action=="REMOVE":
            if props.playblast_index<=len(playblasts)-1:
                playblasts.remove(props.action_index)
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
                playblasts.move(props.playblast_index, target)
                props.playblast_index=target

        # redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PLAYBLASTER_OT_manage_actions)

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_OT_manage_actions)