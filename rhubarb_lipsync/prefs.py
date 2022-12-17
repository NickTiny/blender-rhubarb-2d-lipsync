import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty
from bpy.props import EnumProperty
from platform import system


class RhubarbAddonPreferences(AddonPreferences):
    bl_idname = __package__

    executable_path: StringProperty(
        name="Rhubarb lipsync executable",
        subtype="FILE_PATH",
        default="C:\\Users\\nalbe\AppData\\Roaming\\Blender Foundation\\Blender\\3.3\scripts\\addons\\blender-rhubarb-lipsync\\rhubarb.exe",  # TODO REPLACE
    )  # TODO default path doesn't work when executing from base
    recognizer: EnumProperty(
        name="Recognizer",
        items=[
            (
                "pocketSphinx",
                "pocketSphinx",
                "PocketSphinx is an open-source speech recognition library that generally gives good results for English.",
            ),
            (
                "phonetic",
                "phonetic",
                "This recognizer is language-independent. Use it if your recordings are not in English.",
            ),
        ],
        default="pocketSphinx",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "executable_path")
        layout.prop(self, "recognizer")


def register():
    bpy.utils.register_class(RhubarbAddonPreferences)


def unregister():
    bpy.utils.unregister_class(RhubarbAddonPreferences)
