import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator, get_prism_core_utils_active


class VIEW3D_PT_UI_Export(bpy.types.Panel):
    bl_label = "Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        props = context.scene.move_props
        status_row = box.row()
        status_row.enabled = False


        if get_prism_core_utils_active():
            status_row.label(text="Prism Core Utils is active", icon="LINKED")
        else:
            status_row.label(text="not connected to prism, manual export", icon="UNLINKED")
            box.prop(props, "directory", text="Path")

        
        # list of actions from selected rig
        list_box = box.box()
        list_box.label(text="Actions in Target Rig:")
        action_row = list_box.column()
        action_row.scale_y = 1
        action_row.enabled = False
        actions = self.get_actions_for_rig(props["target_rig"])

        for action in actions:
            action_row.separator(type='LINE')
            action_row.label(text=action.name)

        # Export Button
        row = box.row()
        row.scale_y = 1.5
        row.operator(get_operator("export"), text="Export", icon="EXPORT")

        row.operator(get_operator("generate_def_arm"), text="Generate Deform Armature", icon="ARMATURE_DATA")



    def get_actions_for_rig(self, rig):
        if not rig:
            return []
        
        if rig.type != 'ARMATURE':
            raise TypeError(f"{rig.name} is not an armature")

        actions = set()

        for action in bpy.data.actions:
            actions.add(action)
        return list(actions)
