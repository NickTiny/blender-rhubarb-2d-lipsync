import bpy


# List to store avaliable target properties
prop_list = []


def find_target_and_refresh_properties(context):
    """Returns target's object and updates list
    of avaliable target properties from the target
    to populate target property list"""
    prop_list.clear()
    target, object = get_target(context)
    if target:
        get_target_properties(context.window_manager.rhubarb_panel_settings, target)
    return object


def get_target(context):
    """Returns target item, based on user selected obj_mode."""
    sc = context.scene
    obj = context.active_object
    rhubarb = context.window_manager.rhubarb_panel_settings
    if rhubarb.obj_modes == "bone" and obj.type == "ARMATURE":
        return obj.pose.bones.get(sc.bone_selection), obj
    if rhubarb.obj_modes == "timeoffset":
        target = obj.grease_pencil_modifiers
        return target, obj
    else:
        target = context.object
        return target, obj


def get_target_properties(rhubarb_settings, target):
    """Update items in target props list"""
    # Reset list and append avaliable properties
    for prop_name, _ in target.items():
        # if GPencil find TimeOffset modifier's offset property
        if rhubarb_settings.obj_modes != "timeoffset":
            if "int" in str(type(target[f"{prop_name}"])):
                prop_list.append(
                    (
                        prop_name,
                        prop_name,
                        f"Integer '{prop_name}' on object '{target.id_data.name}' ",
                    )
                )
            if "float" in str(type(target[f"{prop_name}"])):
                prop_list.append(
                    (
                        prop_name,
                        prop_name,
                        f"Float '{prop_name}' on object '{target.id_data.name}' ",
                    )
                )
        else:
            prop_list.append(
                (
                    prop_name,
                    prop_name,
                    f"Modifier '{prop_name}' on grease pencil object '{target.id_data.name}' ",
                )
            )


def initilize_mouth_values(rig_settings):
    """Integer Properties must be initilized if they are not already set to a value
    NOTE: Default value on prop doesn't return as integer until user resets integer to default."""
    # if a single setting is set do not initilie props
    mouth_shapes = (
        "mouth_a",
        "mouth_b",
        "mouth_c",
        "mouth_d",
        "mouth_e",
        "mouth_f",
        "mouth_g",
        "mouth_h",
        "mouth_x",
    )
    initilized = True
    for index, mouth in enumerate(mouth_shapes):
        if not rig_settings.get(mouth):
            initilized = False
    if initilized:
        return

    for index, mouth in enumerate(mouth_shapes):
        if not rig_settings.get(mouth):
            rig_settings[mouth] = index + 1


def debugger(msg):
    print(f"Blender Rhubarb Lip Sync: {msg}")
