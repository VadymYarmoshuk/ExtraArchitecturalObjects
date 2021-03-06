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

#  Extra Architectural Objects
#  Mesh Generator add-on for Blender 3.00
#  (c) 2021 Vadym Yarmoshuk (so_records)

# ----------------------------------- Add-on ----------------------------------- ADD-ON
'''
    Lista która zawiera dane o modułe
'''
bl_info = {
    "name": "Extra Architectural Objects",
    "author": "Vadym Yarmoshuk",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Add > Mesh",
    "description": "Add extra mesh object types",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",  
    "category": "Add Mesh"
}


# ---------------------------------- IMPORT ------------------------------------ IMPORT
'''
    Importuje biblioteki Pythona, Blendera oraz własne skrypty
'''
if "bpy" in locals():
    import importlib
    importlib.reload(add_mesh_greek_dorik_column)
    importlib.reload(add_mesh_greek_ionic_column)
    importlib.reload(add_mesh_roman_column)  
    importlib.reload(add_mesh_tuscan_column)
else :
    from . import add_mesh_greek_dorik_column
    from . import add_mesh_greek_ionic_column
    from . import add_mesh_roman_column
    from . import add_mesh_tuscan_column

import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Menu



class VIEW3D_MT_mesh_architekture_add(Menu):
    '''
        Klasa tworzy VIEW3D folder "Architekture" w foldzerze Mesh,
        która będzie zawierać folderzy Column oraz Piedestal
    '''
    bl_idname = "VIEW3D_MT_mesh_architekture_add"
    bl_label = "Architekture"

    def draw(self, context):
        '''
            Funkcja dodaje do menu Mesh folder Architekture
        '''
        layout = self.layout
        #Podczas wywoływanua operatora przekazuje kontekst wykonania
        layout.operator_context = 'INVOKE_REGION_WIN'
        #Dodjemy folder Column w folder Architekture
        layout.menu("VIEW3D_MT_mesh_column_add",
                text="Column")
        layout.separator()

# -------------------------------- UI Panels  ---------------------------------- PANELS


class VIEW3D_MT_mesh_column_add(Menu):
    '''
        Klasa tworzy folder "Column" w foldzerze Architekture,
        która będzie zawierać funkcje tworzenia różnych column
    '''
    #Tworzymy folder Column
    bl_idname = "VIEW3D_MT_mesh_column_add"
    bl_label = "Column" 

    def draw(self, context):
        '''
            Funkcja dodaje do menu Architekture folder Column
            oraz dodaje funkcji tworzenia column w folder Column 
        '''
        layout = self.layout
        #Podczas wywoływanua operatora przekazuje kontekst wykonania
        layout.operator_context = 'INVOKE_REGION_WIN'

        #Tworzymy przyciski które wywolują funkcji tworzenia kolumn
        oper = layout.operator("mesh.primitive_greekdorikcolumn_add",
                        text="Greek Doric Column", icon="MESH_CYLINDER")
        oper.change = False
        oper = layout.operator("mesh.primitive_greekioniccolumn_add",
                        text="Greek Ionic Column", icon="MESH_CYLINDER")
        oper.change = False
        oper = layout.operator("mesh.primitive_romancolumn_add",
                        text="Roman Column", icon="MESH_CYLINDER")
        oper.change = False
        oper = layout.operator("mesh.primitive_tuscancolumn_add",
                        text="Tuscan Column", icon="MESH_CYLINDER")
        oper.change = False
        layout.separator()

def menu_func(self, context):
    '''
        Tworzymy menu moduły
    '''
    layout = self.layout
    #Podczas wywoływanua operatora przekazuje kontekst wykonania
    layout.operator_context = 'INVOKE_REGION_WIN'

    layout.separator()
    #Dodjemy folder Architekture
    layout.menu("VIEW3D_MT_mesh_architekture_add",
                text="Architekture")


def Extras_contex_menu(self, context):
    '''
        Dodajemy do paska Object Context Menu menu Change, które będzie pozwalać
        zmieniać paramentry.
    '''
    # Imie funkcji Change 
    bl_label = 'Change'

    obj = context.object
    layout = self.layout
    # Spawdzamy który objekt jest storzony
    if obj == None or obj.data is None:
        #Jezełi nie ma objektu, nic nie zwracamy
        return

    if 'Grek Doric Column' in obj.data.keys():
        props = layout.operator("mesh.primitive_greekdorikcolumn_add", text="Change Greek Doric Column")
        props.change = True
        #Pobieramy po jednemy wszystkie paramentry
        for prm in add_mesh_greek_dorik_column.GreekDoricColumnParameters():
            #zapisujemy parametr
            setattr(props, prm, obj.data[prm])
        layout.separator()  
    
    if 'Greek Ionic Column' in obj.data.keys():
        props = layout.operator("mesh.primitive_greekioniccolumn_add", text="Change Greek Ionic Column")
        props.change = True
         #Pobieramy po jednemy wszystkie paramentry
        for prm in add_mesh_greek_ionic_column.GreekIonicColumnParameters():
            setattr(props, prm, obj.data[prm])
            #zapisujemy parametr
        layout.separator()  

    if 'Roman Column' in obj.data.keys():
        props = layout.operator("mesh.primitive_romancolumn_add", text="Change Roman Column")
        props.change = True
        #Pobieramy po jednemy wszystkie paramentry
        for prm in add_mesh_roman_column.RomanColumnParameters():
            setattr(props, prm, obj.data[prm])
            #zapisujemy parametr
        layout.separator()   
    
    if 'Tuscan Column' in obj.data.keys():
        props = layout.operator("mesh.primitive_tuscancolumn_add", text="Change Tuscan Column")
        props.change = True
         #Pobieramy po jednemy wszystkie paramentry
        for prm in add_mesh_greek_dorik_column.TuscanColumnParameters():
            setattr(props, prm, obj.data[prm])
            #zapisujemy parametr
        layout.separator()   

# --------------------------------- Register ----------------------------------- REGISTER
'''
    Lista która będzie zawierać klasy        
'''
classes = [
    VIEW3D_MT_mesh_architekture_add,
    VIEW3D_MT_mesh_column_add,
    add_mesh_greek_dorik_column.AddGreekDoricColumn,
    add_mesh_greek_ionic_column.AddGreekIonicColumn,
    add_mesh_roman_column.AddRomanColumn,
    add_mesh_tuscan_column.AddTuscanColumn,
]

'''
    Funkcja rejestracji wszystkich klas
'''
def register():
    for cls in classes:
        register_class(cls)

    # Dodaje menu „Extra” do menu „Add Mesh” i menu kontekstowego.
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(Extras_contex_menu)

'''
    Funkcja wycofania wszystkich klas
'''
def unregister():
    # Usuwa menu „Extra” z menu „Add Mesh” i menu kontekstowego.
    bpy.types.VIEW3D_MT_object_context_menu.remove(Extras_contex_menu)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

    for cls in reversed(classes):
        unregister_class(cls)

# ----------------------------------- Test ------------------------------------- TEST
'''
    Funkcja która włącza modułe
'''
if __name__ == "__main__":
    register()
