'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
 "name": "Playblaster",
 "author": "Samy Tichadou (tonton)",
 "version": (1, 0),
 "blender": (2, 80, 0),
 "location": "Properties > Font > Font selection",
 "description": "Quick Playblast of your Animation",
  "wiki_url": "https://github.com/samytichadou/FontSelector_blender_addon/wiki",
 "tracker_url": "https://github.com/samytichadou/FontSelector_blender_addon/issues/new",
 "category": "Animation"}


import bpy


# IMPORT SPECIFICS
##################################

from .render_operator import PlayblasterRenderOperator
from .preferences import PlayblasterAddonPrefs
from .modal_check import PlayblasterModalCheck
from .set_preferences_operator import PlayblasterSetPreferences


# register
##################################

classes = (PlayblasterRenderOperator,
            PlayblasterAddonPrefs,
            PlayblasterModalCheck,
            PlayblasterSetPreferences
            )

def register():

    ### OPERATORS ###

    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPS ###

    bpy.types.Scene.playblaster_render_engine = \
        bpy.props.EnumProperty(
                        name = "Engine",
                        default = 'BLENDER_EEVEE',
                        items = (
                        ('BLENDER_WORKBENCH', "Workbench", ""),
                        ('BLENDER_EEVEE', "EEVEE", ""),
                        ))

    bpy.types.Scene.playblaster_resolution_percentage = \
        bpy.props.IntProperty(name = "Resolution Percentage", default = 50, min = 1, max = 100)

    bpy.types.Scene.playblaster_use_compositing = \
        bpy.props.BoolProperty(name = "Compositing", default = False)

    bpy.types.Scene.playblaster_eevee_samples = \
        bpy.props.IntProperty(name = "EEVEE Samples", default = 16, min = 4, max = 128)

    bpy.types.Scene.playblaster_eevee_dof = \
        bpy.props.BoolProperty(name = "EEVEE DoF", default = False)


    bpy.types.Scene.playblaster_is_rendering = \
        bpy.props.BoolProperty()

    bpy.types.Scene.playblaster_completion = \
        bpy.props.IntProperty(min = 0, max = 100)

def unregister():

    ### OPERATORS ###

    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPS ###

    del bpy.types.Scene.playblaster_render_engine
    del bpy.types.Scene.playblaster_resolution_percentage
    del bpy.types.Scene.playblaster_use_compositing
    del bpy.types.Scene.playblaster_eevee_samples
    del bpy.types.Scene.playblaster_eevee_dof

    del bpy.types.Scene.playblaster_is_rendering
    del bpy.types.Scene.playblaster_completion
