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
 "version": (2, 2, 2),
 "blender": (3, 0, 0),
 "location": "Search Menu",
 "description": "Quick Playblast of your Animation",
 "wiki_url": "https://github.com/samytichadou/Playblaster/wiki",
 "tracker_url": "https://github.com/samytichadou/Playblaster/issues/new",
 "category": "Animation"}


# register
##################################

from . import (
    addon_preferences,
    properties,
    gui,
    manage_playblasts_operator,
    render_operator,
    play_operator,
    open_folder_operator,
)

def register():
    properties.register()
    addon_preferences.register()
    gui.register()
    manage_playblasts_operator.register()
    render_operator.register()
    play_operator.register()
    open_folder_operator.register()

def unregister():
    properties.unregister()
    addon_preferences.unregister()
    gui.unregister()
    manage_playblasts_operator.unregister()
    render_operator.unregister()
    play_operator.unregister()
    open_folder_operator.unregister()