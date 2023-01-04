bl_info = {
    "name": "camCage",
    "author": "lymanzhao",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "localtion": "View3D > N",
    "description":"自动创建环绕物体一周的摄影机，默认42个",
    "category": "Camera",
}

import bpy
import os

from bpy.types import (Operator,Panel,Menu)



import mathutils
import math


ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]
ENUM_Side = [("FRONT","Front","Front"), ("TOP","Top","Top")]

class Add_CamCage(bpy.types.Operator):
    bl_idname = "object.add_camcage"
    bl_label = "camCage"
    bl_options = {'UNDO', 'REGISTER'}

    Top: bpy.props.BoolProperty(default=True)
    Quarter: bpy.props.BoolProperty(default=True)
    Bottom: bpy.props.BoolProperty(default=True)
    Size: bpy.props.FloatProperty(default=10)
    link_camera: bpy.props.BoolProperty(default=True)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Size", text="尺寸")
        layout.prop(self, "Top", text="顶部")
        layout.prop(self, "Quarter", text="四分")
        layout.prop(self, "Bottom", text="底部")
        layout.prop(self, "link_camera", text="Link Camera")

    def create_cage_camera(self, context, name, rotation, data=None):

        if data:
            camera = data
        else:
            camera = bpy.data.cameras.new(name)

        object = bpy.data.objects.new(name, camera)
        context.collection.objects.link(object)

        object.rotation_euler = rotation

        object.lock_location[0] = True
        object.lock_location[1] = True
        object.lock_location[2] = True

        object.lock_rotation[0] = True
        object.lock_rotation[1] = True
        object.lock_rotation[2] = True

        object.lock_scale[0] = True
        object.lock_scale[1] = True
        object.lock_scale[2] = True


        return object


    def execute(self, context):

        scn = context.scene
        render = scn.render
        object = None

        bpy.ops.object.select_all(action='DESELECT')

        link_camera = None

        if self.link_camera:
            link_camera = bpy.data.cameras.new("Cameras")

        Camera_cage_Empty = bpy.data.objects.new("camcage", None)
        Camera_cage_Empty.empty_display_type = "SPHERE"
        context.collection.objects.link(Camera_cage_Empty)
        Camera_cage_Empty.select_set(True)
        bpy.context.view_layer.objects.active = Camera_cage_Empty

        Direction_Angle = {}

        Direction_Angle["Front"] = (90, 0, 0)
        Direction_Angle["Right"] = (90, 0, 90)
        Direction_Angle["Back"] = (90, 0, 180)
        Direction_Angle["Left"] = (90, 0, 270)

        if self.Quarter:
            Direction_Angle["Quarter_Front_Right"] = (90, 0, 45)
            Direction_Angle["Quarter_Back_Right"] = (90, 0, 135)
            Direction_Angle["Quarter_Back_Left"] = (90, 0, 225)
            Direction_Angle["Quarter_Front_Left"] = (90, 0, 315)

        if self.Top:
            Direction_Angle["Top"] = (0, 0, 0)
            Direction_Angle["Top_Front"] = (45, 0, 0)
            Direction_Angle["Top_Right"] = (45, 0, 90)
            Direction_Angle["Top_Back"] = (45, 0, 180)
            Direction_Angle["Top_Left"] = (45, 0, 270)

            if self.Quarter:
                Direction_Angle["Top_Quarter_Front_Left"] = (45, 0, 315)
                Direction_Angle["Top_Quarter_Front_Right"] = (45, 0, 45)
                Direction_Angle["Top_Quarter_Back_Right"] = (45, 0, 135)
                Direction_Angle["Top_Quarter_Back_Left"] = (45, 0, 225)
                Direction_Angle["Top_Quarter_Front_Left_675"] = (67.5, 0, 315)
                Direction_Angle["Top_Quarter_Front_Righ_675t45"] = (67.5, 0, 45)
                Direction_Angle["Top_Quarter_Front_Righ_675t90"] = (67.5, 0, 90)
                Direction_Angle["Top_Quarter_Back_Right_675"] = (67.5, 0, 135)
                Direction_Angle["Top_Quarter_Front_Righ_675t180"] = (67.5, 0, 180)
                Direction_Angle["Top_Quarter_Back_Left_675"] = (67.5, 0, 225)
                Direction_Angle["Top_Quarter_Front_Righ_675t270"] = (67.5, 0, 270)
                Direction_Angle["Top_Quarter_Front_Righ_675t360"] = (67.5, 0, 360)

        if self.Bottom:
            Direction_Angle["Bottom"] = (180, 0, 0)
            Direction_Angle["Bottom_Front"] = (135, 0, 0)
            Direction_Angle["Bottom_Right"] = (135, 0, 90)
            Direction_Angle["Bottom_Back"] = (135, 0, 180)
            Direction_Angle["Bottom_Left"] = (135, 0, 270)


            if self.Quarter:
                Direction_Angle["Bottom_Quarter_Front_Right"] = (135, 0, 45)
                Direction_Angle["Bottom_Quarter_Back_Right"] = (135, 0, 135)
                Direction_Angle["Bottom_Quarter_Back_Left"] = (135, 0, 225)
                Direction_Angle["Bottom_Quarter_Front_Left"] = (135, 0, 315)
                Direction_Angle["Bottom_Quarter_Front_Left_112"] = (112.5, 0, 315)
                Direction_Angle["Bottom_Quarter_Front_Righ_112t45"] = (112.5, 0, 45)
                Direction_Angle["Bottom_Quarter_Front_Righ_112t90"] = (112.5, 0, 90)
                Direction_Angle["Bottom_Quarter_Back_Right_112"] = (112.5, 0, 135)
                Direction_Angle["Bottom_Quarter_Front_Righ_112t180"] = (112.5, 0, 180)
                Direction_Angle["Bottom_Quarter_Back_Left_112"] = (112.5, 0, 225)
                Direction_Angle["Bottom_Quarter_Front_Righ_112t270"] = (112.5, 0, 270)
                Direction_Angle["Bottom_Quarter_Front_Righ_112t360"] = (112.5, 0, 360)

        Cameras = []

        for name, rotation_degree in Direction_Angle.items():

            rotation_radians = (math.radians(rotation_degree[0]), math.radians(rotation_degree[1]), math.radians(rotation_degree[2]))
            Camera = self.create_cage_camera(context, name, rotation_radians, data=link_camera)
            Cameras.append(Camera)

        context.view_layer.update()

        for Camera in Cameras:
            Distance = 1
            Camera.location = Camera.matrix_world @ mathutils.Vector((0, 0, Distance))
            Camera.select_set(True)




            context.view_layer.update()
            mw = Camera.matrix_world.copy()
            Camera.parent = Camera_cage_Empty
            Camera.matrix_world = mw

            Constraint = Camera.constraints.new("LIMIT_SCALE")

            Constraint.use_min_x = True
            Constraint.use_min_y = True
            Constraint.use_min_z = True

            Constraint.min_x = 1
            Constraint.min_y = 1
            Constraint.min_z = 1

            Constraint.use_max_x = True
            Constraint.use_max_y = True
            Constraint.use_max_z = True

            Constraint.max_x = 1
            Constraint.max_y = 1
            Constraint.max_z = 1


        Camera_cage_Empty.scale = (self.Size, self.Size, self.Size)
        Camera_cage_Empty.location = context.scene.cursor.location

        return {'FINISHED'}






# 就一个加对象的命令，感觉NPanel用处不大，默认注释掉吧
# class PT_camCage(bpy.types.Panel):
#     bl_label = "camCage"
#     bl_idname ="PT_camCagePanel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = "Camera"

#     def draw(self, context):
#       layout = self.layout

#       obj = context.object

#       col = layout.row()

#       col.operator(Add_CamCage.bl_idname, text="camCage", icon="VIEW_CAMERA")


def menu_func(self, context):
    self.layout.operator(Add_CamCage.bl_idname)




from bpy.utils import register_class,unregister_class



classes = [Add_CamCage]
# classes = [Add_CamCage,PT_camCage]  # 启用NPanel代码的时候使用


def register():
  for cls in classes:
    bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_add.append(menu_func)



def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
