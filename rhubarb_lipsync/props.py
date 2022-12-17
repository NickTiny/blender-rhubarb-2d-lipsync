import bpy
from rhubarb_lipsync.core import (
    prop_list,
)

# Generate list of items from target's props
def enum_items_generator(self, context):
    enum_items = []
    for e, d in enumerate(prop_list):
        enum_items.append((d[0], d[0], d[0], e))
    return enum_items


def mode_options_generator(self, context):
    obj_enum = (
        "obj",
        "Object",
        "Keyframe integer or float property on any object's data",
        "OBJECT_DATA",
        1,
    )
    bone_enum = (
        "bone",
        "Bone",
        "Keyframe integer or float property on any bone in Pose Mode",
        "BONE_DATA",
        2,
    )
    timeoffset_enum = (
        "timeoffset",
        "TimeOffset",
        "Directly keyframe time offset modifier",
        "MOD_TIME",
        3,
    )

    if (
        context.active_object.type == "GPENCIL"
        and context.object.grease_pencil_modifiers.items() != []
    ):
        mode_items = [
            obj_enum,
            timeoffset_enum,
        ]
        return mode_items
    if context.active_object.type == "ARMATURE":
        mode_items = [
            obj_enum,
            bone_enum,
        ]
        return mode_items
    else:
        mode_items = [
            obj_enum,
        ]
        return mode_items


class Rhubarb_Panel_Settings(bpy.types.PropertyGroup):
    """definitions for rhubarb properties"""

    # TODO these are all set to zero because user must manually initilize them.
    mouth_a: bpy.props.IntProperty(name="moutha", default=0)
    mouth_b: bpy.props.IntProperty(name="mouthb", default=0)
    mouth_c: bpy.props.IntProperty(name="mouthc", default=0)
    mouth_d: bpy.props.IntProperty(name="mouthd", default=0)
    mouth_e: bpy.props.IntProperty(name="mouthe", default=0)
    mouth_f: bpy.props.IntProperty(name="mouthf", default=0)
    mouth_g: bpy.props.IntProperty(name="mouthg", default=0)
    mouth_h: bpy.props.IntProperty(name="mouthh", default=0)
    mouth_x: bpy.props.IntProperty(name="mouthx", default=0)

    # rhubarb executable dependcies
    sound_file: bpy.props.StringProperty(name="sound_file", subtype="FILE_PATH")
    dialog_file: bpy.props.StringProperty(name="dialog_file", subtype="FILE_PATH")
    start_frame: bpy.props.IntProperty(name="start_frame")
    presets: bpy.props.EnumProperty(
        items=enum_items_generator, name="Select Target Property"
    )

    obj_modes: bpy.props.EnumProperty(
        name="Select mode",
        items=mode_options_generator,
        description="Run Rhubarb Lipsync in",
    )


classes = (Rhubarb_Panel_Settings,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.rhubarb_panel_settings = bpy.props.PointerProperty(
        type=Rhubarb_Panel_Settings
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.rhubarb_panel_settings
