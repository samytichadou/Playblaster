import bpy


class PLAYBLASTER_PR_playblast_settings(bpy.types.PropertyGroup):
    # Render
    render_type: bpy.props.EnumProperty(
        name = "Render Type",
        default = 'OPENGL',
        items = (
        ('OPENGL', "Open GL", ""),
        ('OPENGLKEY', "Open GL Keyed", ""),
        ),
    )
    shading: bpy.props.EnumProperty(
        name = "Shading Type",
        default = 'MATERIAL',
        items = (
        ('WIREFRAME', "Wireframe", ""),
        ('SOLID', "Solid", ""),
        ('MATERIAL', "Material", ""),
        ('RENDERED', "Rendered", ""),
        ),
    )
    preselection: bpy.props.EnumProperty(
        name = "Select",
        default = 'ALL',
        items = (
        ('ALL', "All", ""),
        ('NONE', "None", ""),
        ),
    )
    eevee_samples: bpy.props.IntProperty(name = "EEVEE Samples", default = 8, min = 4, max = 128)
    eevee_ambient_occlusion: bpy.props.BoolProperty(name = "EEVEE AO", default = False)
    
    simplify: bpy.props.BoolProperty(name = "Simplify", default = True)
    simplify_subdivision: bpy.props.IntProperty(name = "Max Subdivision", default = 0, min = 0, max = 6)
    simplify_particles: bpy.props.FloatProperty(name = "Max Child Particles", default = 0, min = 0, max = 1)

    show_overlays: bpy.props.BoolProperty(name = "Show Overlays")

    # Output
    resolution_percentage: bpy.props.IntProperty(name = "Resolution Percentage", default = 50, min = 1, max = 100)
    frame_range_type: bpy.props.EnumProperty(
        name = "Frame Range",
        default = 'SCENE',
        items = (
        ('SCENE', "Scene Frame Range", ""),
        ('PREVIEW', "Preview Frame Range", ""),
        ('OVERRIDE', "Overriden Frame Range", ""),
        ),
    )
    frame_range_in: bpy.props.IntProperty(name = "Start Frame", min = 0, default = 1)
    frame_range_out: bpy.props.IntProperty(name = "End Frame", min = 1, default = 100)
    use_compositing: bpy.props.BoolProperty(name = "Compositing", default = False)
    use_3dviewport: bpy.props.BoolProperty(name = "Use 3D View", default = False)

    end_action: bpy.props.EnumProperty(
        name = "End Action",
        default = 'PLAY',
        items = (
        ('PLAY', "Play Video", ""),
        ('NOTHING', "Do Nothing", ""),
        ),
    )

    player: bpy.props.EnumProperty(
        name = "Player",
        default = 'DEFAULT',
        items = (
        ('DEFAULT', "Default Player", ""),
        ('BLENDER', "Blender Player", ""),
        #('SPECIFIC', "Specific Player", ""),
        ),
    )

    rendered_filepath: bpy.props.StringProperty()
    hash: bpy.props.StringProperty()


class PLAYBLASTER_PR_playblaster_properties(bpy.types.PropertyGroup):
    playblasts: bpy.props.CollectionProperty(type = PLAYBLASTER_PR_playblast_settings, name="Playblast Settings")
    playblast_index: bpy.props.IntProperty(default = -1, min = -1)


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