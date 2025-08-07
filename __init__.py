from . import ops, props, ui, prefs

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
