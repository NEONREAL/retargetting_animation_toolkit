from typing import ValuesView
import bpy  # type: ignore

# preferences
from .preferences import Sample_Preferences
from .misc.MoveProps import MoveProps

# Operators
from .operators.OBJECT_OT_PickObject import OBJECT_OT_PickObject
from .operators.OBJECT_OT_BakeAnimation import OBJECT_OT_BakeAnimation
from .operators.OBJECT_OT_FixScale import OBJECT_OT_FixScale
from .operators.FILE_OT_Export import FILE_OT_Export
from .operators.OBJECT_OT_GenerateDeformArmature import OBJECT_OT_GenerateDeformArmature
from .operators.ANIM_OT_Pin import ANIM_OT_Pin

# panels
from .panels.VIEW3D_PT_UI_Retargetting import VIEW3D_PT_UI_Retargetting
from .panels.VIEW3D_PT_UI_Animating import VIEW3D_PT_UI_Animating

# reading values such as name, version and more from toml so there is no need to change information in two places
def load_manifest_info():
    from .constants import get_manifest

    manifest = get_manifest()

    # reading addon name
    extension_name = manifest["name"]

    # reading addon version
    version_str = manifest["version"]
    version_tuple = tuple(int(x) for x in version_str.split("."))

    # reading Blender version
    blender_version_str = manifest["blender_version_min"]
    blender_version_tuple = tuple(int(x) for x in blender_version_str.split("."))

    bl_info = {
        "name": extension_name,
        "version": version_tuple,
        "blender": blender_version_tuple,
    }

    return bl_info


blender_manifest = load_manifest_info()
bl_info = {
    "name": blender_manifest["name"],
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Your Name",
    "version": blender_manifest["version"],
    "blender": blender_manifest["blender"],
    "location": "Npanel",
    "support": "COMMUNITY",
    "category": "UI",
}

classes = [
    # preferences
    Sample_Preferences,
    MoveProps,
    # operators:
    OBJECT_OT_PickObject,
    OBJECT_OT_BakeAnimation,
    OBJECT_OT_FixScale,
    OBJECT_OT_GenerateDeformArmature,
    FILE_OT_Export,
    ANIM_OT_Pin,
    # panels:
    VIEW3D_PT_UI_Retargetting,
    VIEW3D_PT_UI_Animating,
]


def register():
    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.Scene.move_props = bpy.props.PointerProperty(type=MoveProps)
    


def unregister():
    del bpy.types.Scene.move_props
    for i in reversed(classes):
        bpy.utils.unregister_class(i)
