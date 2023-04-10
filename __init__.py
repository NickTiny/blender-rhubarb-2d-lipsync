from . import ops, props, ui, prefs

"""Forked from https://github.com/scaredyfish/blender-rhubarb-lipsync/"""

__version__ = "4.0.0"

bl_info = {
    "name": "Blender Rhubarb 2D Lipsync",
    "author": "By Nick Alberelli, forked from Addon by Andrew Charlton, includes Rhubarb Lip Sync by Daniel S. Wolf",
    "version": (4, 0, 2),
    "blender": (3, 0, 0),
    "location": "VIEW3D > Sidebar > Rhubarb 2D Lipsync",
    "description": "Integrate Rhubarb Lipsync into Blender",
    "wiki_url": "https://github.com/NickTiny/blender-rhubarb-2d-lipsync",
    "tracker_url": "https://github.com/NickTiny/blender-rhubarb-2d-lipsync/issues",
    "support": "COMMUNITY",
    "category": "Animation",
}


def register():
    ops.register()
    ui.register()
    props.register()
    prefs.register()


def unregister():
    ops.unregister()
    ui.unregister()
    props.unregister()
    prefs.unregister()
