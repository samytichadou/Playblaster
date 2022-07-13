import bpy


class PLAYBLASTER_PR_playblast_settings(bpy.types.PropertyGroup):
    render_type: bpy.props.EnumProperty(
        name = "Render Type",
        default = 'OPENGLKEY',
        items = (
        ('FULL', "Classic Render", ""),
        ('OPENGL', "Open GL", ""),
        ('OPENGLKEY', "Open GL Keyed", ""),
        ),
    )
    render_engine: bpy.props.EnumProperty(
        name = "Engine",
        default = 'BLENDER_EEVEE',
        items = (
        ('BLENDER_WORKBENCH', "Workbench", ""),
        ('BLENDER_EEVEE', "EEVEE", ""),
        ),
    )
    resolution_percentage: bpy.props.IntProperty(name = "Resolution Percentage", default = 50, min = 1, max = 100)

    frame_range_override: bpy.props.BoolProperty(name = "Frame Range Override", default = False)
    frame_range_in: bpy.props.IntProperty(name = "Start Frame", min = 0, default = 1)
    frame_range_out: bpy.props.IntProperty(name = "End Frame", min = 1, default = 100)
    
    use_compositing: bpy.props.BoolProperty(name = "Compositing", default = False)
    
    eevee_samples: bpy.props.IntProperty(name = "EEVEE Samples", default = 8, min = 4, max = 128)
    eevee_ambient_occlusion: bpy.props.BoolProperty(name = "EEVEE AO", default = False)
    
    simplify: bpy.props.BoolProperty(name = "Simplify", default = True)
    simplify_subdivision: bpy.props.IntProperty(name = "Max Subdivision", default = 0, min = 0, max = 6)
    simplify_particles: bpy.props.FloatProperty(name = "Max Child Particles", default = 0, min = 0, max = 1)


class PLAYBLASTER_PR_playblaster_properties(bpy.types.PropertyGroup):
    playblast_settings:   bpy.props.PointerProperty(type = PLAYBLASTER_PR_playblast_settings, name="Playblast Settings")


### REGISTER ---
def register():
    bpy.utils.register_class(PLAYBLASTER_PR_playblast_settings)
    bpy.utils.register_class(PLAYBLASTER_PR_playblaster_properties)
    bpy.types.Scene.playblaster_properties = \
        bpy.props.PointerProperty(type = PLAYBLASTER_PR_playblaster_properties, name="Playblaster")

def unregister():
    bpy.utils.unregister_class(PLAYBLASTER_PR_playblast_settings)
    bpy.utils.unregister_class(PLAYBLASTER_PR_playblaster_properties)
    del bpy.types.Scene.playblaster_properties