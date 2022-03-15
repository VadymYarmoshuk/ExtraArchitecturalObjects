# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK ##### 
# "author": "Vadym Yamrohsuk"

import bpy
import bmesh
import math 
from bpy.props import (
        FloatProperty,
        IntProperty,
        StringProperty,
        BoolProperty,
        )
from mathutils import (
        Quaternion,
        Vector,
        )
from bpy_extras import object_utils
static_radius = 0.0
static_width = 0.0

def create_circle(segments, radius, width):
    vertices = []
    for i in range(segments):
        angle = (math.pi*2) * i / segments
        vertices.append((radius * math.cos(angle), radius * math.sin(angle), width))
    return vertices

def create_faces(segments, size_vertices, faces, step):
    step_circle = step * segments
    if step * segments < (size_vertices - segments):
        for i in range(segments):
            pos_1 = i + step_circle
            pos_2 = i + 1 + step_circle  
            pos_3 = segments + i + 1 + step_circle
            pos_4 = segments + i + step_circle
            if i == segments - 1:
                pos_2 = step_circle
                pos_3 = step_circle  + segments
                faces.append(( pos_1 , pos_2 , pos_3, pos_4 ))   
            else: 
                faces.append(( pos_1 , pos_2 , pos_3, pos_4 ))
        step += 1 
        create_faces(segments, size_vertices, faces, step)       
    else:
        pass

def greek_column_mesh(self, context):

    if (self.radius != static_radius):
        self.width = self.radius * 16
    if (self.width != static_width):
        self.radius = self.width /16
    pol_width = self.radius * 8
    radius_shafl_up = (7 * self.radius) / 8

    pol_width = self.radius * 8
    radius_shafl_up = (7 * self.radius) / 8

    vertices = []
    faces = []
    edges = []
   
    '''Create Vertices Shafl'''
    vertices_shaft_cirlce_down = create_circle(self.segments, self.radius,  -(pol_width))
    vertices_shaft_cirlce_up = create_circle(self.segments, radius_shafl_up,  pol_width - self.radius * 1.1)

    vertices += vertices_shaft_cirlce_down 
    vertices += vertices_shaft_cirlce_up

    '''Create Vertices Helping first element'''
    vertices_help1_cirlce_down = create_circle(self.segments, radius_shafl_up * 1.15,  pol_width - self.radius * 1.1)
    vertices_help1_cirlce_center = create_circle(self.segments, radius_shafl_up * 1.15,  pol_width - self.radius * 1.05)
    vertices_help1_circle_up = create_circle(self.segments, radius_shafl_up * 1.15,  pol_width - self.radius)
    vertices += vertices_help1_cirlce_down
    vertices += vertices_help1_cirlce_center
    vertices += vertices_help1_circle_up

    '''Create Vertices Necking''' 
    vertices_necking_cirlce1 = create_circle(self.segments, radius_shafl_up,  pol_width - self.radius)
    vertices_necking_cirlce2 = create_circle(self.segments, radius_shafl_up,  pol_width - self.radius * 0.8)

    vertices += vertices_necking_cirlce1 
    vertices += vertices_necking_cirlce2

    '''Create Vertices Helping second element'''
    vertices_help2_cirlce_down = create_circle(self.segments, radius_shafl_up * 1.15,  pol_width - self.radius * 0.8)
    vertices_help2_cirlce_center = create_circle(self.segments, radius_shafl_up * 1.15,  pol_width - self.radius * 0.75)
    vertices_help2_cirlce_up = create_circle(self.segments, radius_shafl_up * 1.15,  pol_width - self.radius * 0.70)
    vertices += vertices_help2_cirlce_down
    vertices += vertices_help2_cirlce_center
    vertices += vertices_help2_cirlce_up

    '''Create Echinus Up '''
    vertices_echinus = create_circle(self.segments, radius_shafl_up * 1.32,  pol_width - self.radius * 0.40)

    vertices += vertices_echinus

    vertices_help3_down = create_circle(self.segments, radius_shafl_up * 1.35,  pol_width - self.radius * 0.40)
    vertices_help3_up = create_circle(self.segments, radius_shafl_up * 1.35,  pol_width - self.radius * 0.10)
    vertices += vertices_help3_down
    vertices += vertices_help3_up

    vertices_help4_down = create_circle(self.segments, radius_shafl_up * 1.4,  pol_width - self.radius * 0.10)
    vertices_help4_up = create_circle(self.segments, radius_shafl_up * 1.4,  pol_width )
    vertices += vertices_help4_down
    vertices += vertices_help4_up

    '''Create Faces '''
    create_faces(self.segments, len(vertices), faces, 0)

    mesh = bpy.data.meshes.new("Greek Column")
    mesh.from_pydata(vertices, [], faces)

    static_width = self.width
    static_radius = self.radius

    return mesh



class AddGreekColumn(bpy.types.Operator,  object_utils.AddObjectHelper):
    bl_idname = "mesh.primitive_greekcolumn_add"
    bl_label = "Greek Column"
    bl_description = "Construct a step greek column mesh"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    GreekColumn : BoolProperty(name = "Greek Column",
                default = True,
                description = "Greek Column")
    change : BoolProperty(name = "Change",
                default = False,
                description = "change Greek Column")

    segments: IntProperty(
            name="Vertices",
            description="How many vertices have column",
            min=3,
            max=500,
            default=32,
            )
    radius: FloatProperty(
            name="Radius",
            description="",
            min=0.001,
            max=100,
            default=0.5,
            )
    width: FloatProperty(
            name="Width",
            description="Initial base step width",
            min=0.001,
            max=100,
            default=4,
            )
    generate_uvs: BoolProperty(
        name="Generate UVs",
        description="Generate a default UV map",
        default=True,
    )

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, 'segments', expand=True)
        layout.prop(self, 'radius', expand=True)
        layout.prop(self, 'width', expand=True)

        layout.separator()
        if self.change == False:
            col = layout.column(align=True)
            col.prop(self, 'generate_uvs', expand=True)
            col = layout.column(align=True)
            col.prop(self, 'align', expand=True)
            col = layout.column(align=True)
            col.prop(self, 'location', expand=True)
            col = layout.column(align=True)
            col.prop(self, 'rotation', expand=True)


    def execute(self, context):
        # turn off 'Enter Edit Mode'
        use_enter_edit_mode = bpy.context.preferences.edit.use_enter_edit_mode
        bpy.context.preferences.edit.use_enter_edit_mode = False

        if bpy.context.mode == "OBJECT":
            if context.selected_objects != [] and context.active_object and \
                (context.active_object.data is not None) and ('Greek Column' in context.active_object.data.keys()) and \
                (self.change == True):
                obj = context.active_object
                oldmesh = obj.data
                oldmeshname = obj.data.name
                obj.data = greek_column_mesh(self, context)
                try:
                    bpy.ops.object.vertex_group_remove(all=True)
                except:
                    pass

                for material in oldmesh.materials:
                    obj.data.materials.append(material)

                bpy.data.meshes.remove(oldmesh)
                obj.data.name = oldmeshname
            else:
                mesh = greek_column_mesh(self, context)
                obj = object_utils.object_data_add(context, mesh, operator=self)

            obj.data["Greek Greek Column"] = True
            obj.data["change"] = False
            for prm in GreekColumnParameters():
                obj.data[prm] = getattr(self, prm)

        if bpy.context.mode == "EDIT_MESH":
            active_object = context.active_object
            name_active_object = active_object.name
            bpy.ops.object.mode_set(mode='OBJECT')
            mesh = greek_column_mesh(self, context)
            obj = object_utils.object_data_add(context, mesh, operator=self)

            obj.select_set(True)
            active_object.select_set(True)
            bpy.context.view_layer.objects.active = active_object
            bpy.ops.object.join()
            context.active_object.name = name_active_object
            bpy.ops.object.mode_set(mode='EDIT')

        if use_enter_edit_mode:
            bpy.ops.object.mode_set(mode = 'EDIT')

        # restore pre operator state
        bpy.context.preferences.edit.use_enter_edit_mode = use_enter_edit_mode

        return {'FINISHED'}
def GreekColumnParameters():
    GreekColumnParameters = [
        "segments",
        "radius",
        "width",
        ]
    return GreekColumnParameters
