import bpy  # type: ignore


bones = {
    # Left arm
    "UpperArm.L": ("LeftArm", "COPY_TRANSFORMS"),
    "LowerArm.L": ("LeftForeArm", "COPY_TRANSFORMS"),
    "Hand.L": ("LeftHand", "COPY_TRANSFORMS"),
    # Right arm
    "UpperArm.R": ("RightArm", "COPY_TRANSFORMS"),
    "LowerArm.R": ("RightForeArm", "COPY_TRANSFORMS"),
    "Hand.R": ("RightHand", "COPY_TRANSFORMS"),
    # Left Leg
    "UpperLeg.L": ("LeftUpLeg", "COPY_TRANSFORMS"),
    "LowerLeg.L": ("LeftLeg", "COPY_TRANSFORMS"),
    "Foot.L": ("LeftFoot", "COPY_TRANSFORMS"),
    "Toes.L": ("LeftToeBase", "COPY_ROTATION"),
    # Right Leg
    "UpperLeg.R": ("RightUpLeg", "COPY_TRANSFORMS"),
    "LowerLeg.R": ("RightLeg", "COPY_TRANSFORMS"),
    "Foot.R": ("RightFoot", "COPY_TRANSFORMS"),
    "Toes.R": ("RightToeBase", "COPY_ROTATION"),
}
root_bones = {
    "UpperArm.L-ROOT": ("LeftArm", "COPY_TRANSFORMS"),
    "UpperArm.R-ROOT": ("RightArm", "COPY_TRANSFORMS"),
    "UpperLeg.L-ROOT": ("LeftUpLeg", "COPY_TRANSFORMS"),
    "UpperLeg.R-ROOT": ("RightUpLeg", "COPY_TRANSFORMS"),
}

# Generate FK_ prefixed dictionary
FK_bones = {f"FK-{k}": v for k, v in bones.items()}

# Generate IK_ prefixed dictionary
IK_bones = {f"IK-{k}": v for k, v in bones.items()}


class MoveProps(bpy.types.PropertyGroup):
    Modes = [("edit", "Edit", ""), ("pose", "Pose", "")]

    source_rig: bpy.props.PointerProperty(type=bpy.types.Object, name="Rig")

    target_rig: bpy.props.PointerProperty(type=bpy.types.Object, name="Rig")

    delete: bpy.props.BoolProperty(name="Delete old Property")

    # etc.
