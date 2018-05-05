import bpy
from bpy.props import IntProperty, FloatProperty
import io
import sys
import subprocess
from threading  import Thread
from queue import Queue, Empty
import json


class RhubarbLipsyncOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "object.rhubarb_lipsync"
    bl_label = "Rhubarb lipsync"

    cue_prefix = 'Mouth_'

    def modal(self, context, event):
        try:
            (stdout, stderr) = self.rhubarb.communicate(timeout=1)

            if stdout:
                wm = context.window_manager
                wm.event_timer_remove(self._timer)

                results = json.loads(stdout)
                fps = context.scene.render.fps
                lib = context.object.pose_library

                if not results['mouthCues']: return

                for cue in results['mouthCues']:
                    print("start: {0} frame: {1} value: {2}".format(cue['start'], cue['start'] * fps , cue['value']))

                    pose_index = context.object.pose_library.mouth_shapes['mouth_' + cue['value'].lower()]

                    frame_num = round(cue['start'] * fps)

                    context.scene.frame_set(frame_num)

                    bpy.ops.poselib.apply_pose(pose_index=pose_index)
                    for bone in context.selected_pose_bones:
                        bone.keyframe_insert('location')
                        bone.keyframe_insert('rotation_euler')


                return {'FINISHED'}
        except subprocess.TimeoutExpired as ex:
            return {'PASS_THROUGH'}
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            print(template.format(type(ex).__name__, ex.args))
            return {'CANCELLED'}


    def invoke(self, context, event):
        inputfile = context.object.pose_library.mouth_shapes.sound_file
        dialogfile = context.object.pose_library.mouth_shapes.dialog_file
        self.rhubarb = subprocess.Popen("D:/Cloud/OneDrive/rhubarb/rhubarb.exe -f json --machineReadable --dialogFile %s --extendedShapes GHX %s" % (dialogfile, inputfile),
                                   stdout=subprocess.PIPE, universal_newlines=True)

        wm = context.window_manager
        self._timer = wm.event_timer_add(1, context.window)

        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}



    def finished(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)



def register():
    bpy.utils.register_class(RhubarbLipsyncOperator)


def unregister():
    bpy.utils.unregister_class(RhubarbLipsyncOperator)

if __name__ == "__main__":
    register()

