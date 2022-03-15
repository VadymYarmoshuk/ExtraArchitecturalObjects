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

# ---------------------------------- IMPORT ------------------------------------ IMPORT
'''
    Importuje biblioteki Pythona, Blendera oraz własne skrypty
'''
import bpy
import math 
from bpy.props import (
        FloatProperty,
        IntProperty,
        BoolProperty,
        EnumProperty,
        )
from mathutils import (
        Quaternion,
        Vector,
        )
from bpy_extras import object_utils

# Zmiene globalne zmian parametrów radius oraz głębokość
static_radius = 0.0
static_width = 0.0

def create_circle(segments, radius, width):
    '''
        Fukcja zwracające liste wierzchołek koła
        Segment : liczba ilości wierzchołek
        Radius : dlugość od jednego wirzchołka do centru
        depth : Pozycja koła po osi Z
    '''
    #Lista pusta, która będzie rawierać wierzchołki koła
    vertices = []
    #Pentła przechodząca "segments" razy
    for i in range(segments):
        # Zmiena zawieracjąca kąt do osi x promienia narysowanego od początku do punku(x, y)
        # Jest w przedziałe od 0 do 2*pi
        angle = (math.pi*2) * i / segments
        # Zapisuje na konić vector stworzonego wierzchołka
        vertices.append((radius * math.cos(angle), radius * math.sin(angle), width))
    # Zwaraca liste wierzchołek 
    return vertices

def create_faces(segments, size_vertices, faces, step):
    '''
        Funkcja tworząca płaszczyzny między wierzchołkami 
        za pomocą rekurencji
        Segment :   liczba ilości wierzchołek
        size_vertices:  długość listy zawierającej wierzchołki
        faces : lista do której dopisujemy indeksy płaszczyzn
        step :  liczba zwiększająca się o 1 za każdym przejściem,
                domyślnie równa 0
    '''
    # pobieramy indeksy początek koł
    step_circle = step * segments
    '''
        Sprawdzamy czy nie wyśliśmy za przedział liśty,
        jeżeli nie to tworzymy płaszczyzny między sąsiednimi wierzchołkami
        jeżeli tak to kończymy rekurencje
    '''
    if step * segments < (size_vertices - segments):
        # Przechodzimy po liczbe 
        for i in range(segments):
            # Tworzymy 4 indeksa oraz przepisujemy im dane indeksów wierzchołek
            pos_1 = i + step_circle
            pos_2 = i + 1 + step_circle  
            pos_3 = segments + i + 1 + step_circle
            pos_4 = segments + i + step_circle
            # Przy podejściu do ostatniego wierzchołka koła zmieniamy pozycje 2, 3 indeksów 
            if i == segments - 1:
                pos_2 = step_circle
                pos_3 = step_circle  + segments
                # Zapisujemy do listy "faces" indeksy płaszczyzn
                faces.append(( pos_1 , pos_2 , pos_3, pos_4 ))   
            else: 
                # Zapisujemy do listy "faces" indeksy płaszczyzn
                faces.append(( pos_1 , pos_2 , pos_3, pos_4 ))
        # Powtarzamy funckje z zwiękrzonym zmieną "step" o jeden
        create_faces(segments, size_vertices, faces, step + 1)       
    else:
        # Wychodzimy z rekurencji
        pass

def tuscan_column_mesh(self, context):
    '''
        Funkcja zwraca mesh columny 
    '''
    # Pobieramy dane z globałnych zmienych
    global static_width 
    global static_radius    
    
    '''
        Sprawdzamy czy były zmiany w parametrach 
        Jeżeli zmieniliśmy jeden z parametra radius oraz depth
        to i drugij powinien zwienić się tak jak one są zwizane miedzy sobą
        depth równa się 16 radiusam
    ''' 
    if (self.radius != static_radius):
        self.width = self.radius * 14
    if (self.width != static_width):
        self.radius = self.width /14

    pol_width = self.radius * 7
    radius_shafl_up = (7 * self.radius) / 7

    #Listy, które będą zawirać wierzchołki, krawędzi oraz płaszczyzny
    vertices = []
    faces = []
    edges = []

    # Tworzymy wierzchołki 
    vertices_circle_1 = create_circle(self.segments, self.radius * 1.35,  -(pol_width))
    vertices_circle_2 = create_circle(self.segments, self.radius * 1.35,  -(pol_width - self.radius * 0.35))
    # Dodajemy do listy wierzchołki shaft
    vertices += vertices_circle_1
    vertices += vertices_circle_2

    # Tworzymy wierzchołki 
    vertices_circle_3 = create_circle(self.segments, self.radius * 1.35,  -(pol_width - self.radius * 0.50))
    # Dodajemy do listy wierzchołki shaft
    vertices += vertices_circle_3

    # Tworzymy wierzchołki 
    vertices_circle_4 = create_circle(self.segments, self.radius * 1.3,  -(pol_width - self.radius * 0.50))
    # Dodajemy do listy wierzchołki shaft
    vertices += vertices_circle_4
    # Tworzymy wierzchołki 
    vertices_circle_5 = create_circle(self.segments, self.radius * 1.35,  -(pol_width - self.radius * 0.70))
    # Dodajemy do listy wierzchołki shaft
    vertices += vertices_circle_5

    # Tworzymy wierzchołki 
    vertices_circle_6 = create_circle(self.segments, self.radius * 1.3,  -(pol_width - self.radius * 0.85))
    # Dodajemy do listy wierzchołki shaft
    vertices += vertices_circle_6

    # Tworzymy wierzchołki 
    vertices_circle_7 = create_circle(self.segments, self.radius * 1.26,  -(pol_width - self.radius * 0.85))
    # Dodajemy do listy wierzchołki shaft
    vertices += vertices_circle_7

    # Tworzymy wierzchołki 
    vertices_circle_8 = create_circle(self.segments, self.radius * 1.26,  -(pol_width - self.radius))
    # Dodajemy do listy wierzchołki shaft
    vertices += vertices_circle_8

    # Tworzymy wierzchołki 
    vertices_shaft_circle_down = create_circle(self.segments, self.radius,  -(pol_width - self.radius))
    vertices_shaft_circle_up = create_circle(self.segments, radius_shafl_up ,  pol_width - self.radius * 1.1)
    # Dodajemy do listy wierzchołki shaft
    vertices += vertices_shaft_circle_down 
    vertices += vertices_shaft_circle_up

    # Tworzymy wierzchołki 
    vertices_help_circle_down = create_circle(self.segments, radius_shafl_up,  pol_width - self.radius * 1.3)
    vertices_help_circle_center = create_circle(self.segments, radius_shafl_up * 1.1,  pol_width - self.radius * 1.25)
    vertices_help_circle_center2 = create_circle(self.segments, radius_shafl_up * 1.15,  pol_width - self.radius * 1.15)
    vertices_help_circle_center3 = create_circle(self.segments, radius_shafl_up * 1.1,  pol_width - self.radius * 1.05)
    vertices_help_circle_up = create_circle(self.segments, radius_shafl_up,  pol_width - self.radius)
    # Dodajemy do listy wierzchołki 
    vertices += vertices_help_circle_down
    vertices += vertices_help_circle_center
    vertices += vertices_help_circle_center2
    vertices += vertices_help_circle_center3
    vertices += vertices_help_circle_up

    # Tworzymy wierzchołki 
    vertices_necking_circle1 = create_circle(self.segments, radius_shafl_up,  pol_width - self.radius)
    vertices_necking_circle2 = create_circle(self.segments, radius_shafl_up,  pol_width - self.radius * 0.775)
    # Dodajemy do listy wierzchołki 
    vertices += vertices_necking_circle1 
    vertices += vertices_necking_circle2

    # Tworzymy wierzchołki 
    vertices_help1_circle1 = create_circle(self.segments, radius_shafl_up * 1.125,  pol_width - self.radius* 0.775)
    vertices_help1_circle2 = create_circle(self.segments, radius_shafl_up * 1.125,  pol_width - self.radius * 0.725)
    # Dodajemy do listy wierzchołki 
    vertices += vertices_help1_circle1 
    vertices += vertices_help1_circle2

    # Tworzymy wierzchołki 
    vertices_echinus_down = create_circle(self.segments, radius_shafl_up * 1.1,  pol_width - self.radius * 0.725)
    vertices_echinus_center = create_circle(self.segments, radius_shafl_up * 1.35,  pol_width - self.radius * 0.48)
    vertices_echinus_up = create_circle(self.segments, radius_shafl_up * 1.35,  pol_width - self.radius * 0.5)
    # Dodajemy do listy wierzchołki 
    vertices += vertices_echinus_down
    vertices += vertices_echinus_center
    vertices += vertices_echinus_up

    # Tworzymy wierzchołki 
    vertices_help2_circle_down = create_circle(self.segments, radius_shafl_up * 1.5,  pol_width - self.radius * 0.5)
    vertices_help2_circle_center = create_circle(self.segments, radius_shafl_up * 1.5,  pol_width - self.radius * 0.25)
    vertices_help2_circle_up = create_circle(self.segments, radius_shafl_up * 1.5,  pol_width)
    # Dodajemy do listy wierzchołki 
    vertices += vertices_help2_circle_down
    vertices += vertices_help2_circle_center
    vertices += vertices_help2_circle_up
    
    # Tworzymy oraz dodajemy do listy "faces" płaszczyzny 
    create_faces(self.segments, len(vertices), faces, 0)

    # Zapisujemy stare dane promienia oraz długości do globalnych zmiennych
    static_width = self.width
    static_radius = self.radius

    # Tworzymy nowy mesh
    mesh = bpy.data.meshes.new("Tuscan Column")
    # Tworzymy nową siatekę z listy wierzchołków, krawędzi oraz płaszczyzn
    mesh.from_pydata(vertices, [], faces)

    # Zwracamy stworzony mesh
    return mesh

# -------------------------- Collection PropertyGroup  ------------------------- PROPERTY GROUPS

class AddTuscanColumn(bpy.types.Operator,  object_utils.AddObjectHelper):
    '''
        Klasa 
    '''
    # id po którym będzie wywoływać się klasa 
    bl_idname = "mesh.primitive_tuscancolumn_add"
    # Nazwa klasy
    bl_label = "Tuscan Column"
    # Opis klasy
    bl_description = "Construct a step tuscan column mesh"
    # Opcje które posiada klasa
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # Zmiena przechowywająca imie
    TuscanColumn : BoolProperty(name = "Tuscan Column",
                default = True,
                description = "Tuscan Column")
    # Zmiena która sprawdza czy parametry były zmienione
    change : BoolProperty(name = "Change",
                default = False,
                description = "change Tuscan Column")

    #Zmiena przechowywająca wierzchołki kół 
    segments: IntProperty(
            name="Vertices",
            description="Number of segments for the ring of the column",
            min=3,
            max=500,
            default=32,
            )
    # Zmiena przechowywająca długośc między wierzchołkem koła oraz centrem
    radius: FloatProperty(
            name="Radius",
            description="Radius from the circle to the center of the cross sections",
            min=0.001,
            max=100,
            default=0.5,
            )
    # Zmiena przechowywająca długośc kolumny
    width: FloatProperty(
            name="Width",
            description="Initial base step width",
            min=0.001,
            max=100,
            default=4,
            )
    # Zmiena która będzie tworzyć UV's
    generate_uvs: BoolProperty(
        name="Generate UVs",
        description="Generate a default UV map",
        default=True,
    )

    def draw(self, context):
        layout = self.layout

        '''
            Nastepne polecenie robi:
            * spowoduje to wyrównanie etykiety właściwości do prawej;
            * Jeśli właściwość jest animowalna, np. Enum Properties, Float, Int, 
                to doda animowane kółko po prawej stronie, aby umożliwić animację właściwości.
            * Dla właściwości Float spowoduje to oddzielenie etykiety poza pole 
                wprowadzania zamiast zwykłej etykiety wewnątrz pola wprowadzania.
            *zapewnia to, że etykieta właściwości ma wystarczająco dużo miejsca, 
                aby być wyświetlane w całości, jeśli to możliwe, 
                a następnie daje resztę miejsca do pola wejściowego.
        '''
        layout.use_property_split = True
        # przycisk animacji nie pojawi się
        layout.use_property_decorate = False

        # Tworzymy ślizgacz, dla zmienianie wierzchołek kół
        layout.prop(self, 'segments', expand=True)
        # Tworzymy ślizgacz, dla zmienianie długośc między wierzchołkem koła oraz centrem
        layout.prop(self, 'radius', expand=True)
        # Tworzymy ślizgacz, dla zmienianie długośc kolumny
        layout.prop(self, 'width', expand=True)

        # Dodajemy przecinek
        layout.separator()
        # Sprawdzmy czy nie zmienamy parametry teraz
        if self.change == False:
             # Przycisk tworzący UV's " Jeście nie dokończony "
            col = layout.column(align=True)
            col.prop(self, 'generate_uvs', expand=True)
            # Tablica wybierająca wyrównanie elementa
            col = layout.column(align=True)
            col.prop(self, 'align', expand=True)
            # Tworzymy 3 ślizgacza( oś X, Y, Z), żeby przesuwać element po macierzy według osiej
            col = layout.column(align=True)
            col.prop(self, 'location', expand=True)
            # Tworzymy 3 ślizgacza( oś X, Y, Z), żeby przekręcać element po macierzy według osiej 
            col = layout.column(align=True)
            col.prop(self, 'rotation', expand=True)


    def execute(self, context):
        '''
            Głowna funkcja wywołyjąca, kiedy jest włączone polecenie klasy "bl_idname"
        '''
        # wyłącza opcje 'Enter Edit Mode'
        use_enter_edit_mode = bpy.context.preferences.edit.use_enter_edit_mode
        bpy.context.preferences.edit.use_enter_edit_mode = False

        # Sprawdzamy w jakim trybie jesteśmy
        if bpy.context.mode == "OBJECT":
            if context.selected_objects != [] and context.active_object and \
                (context.active_object.data is not None) and ('Tuscan Column' in context.active_object.data.keys()) and \
                (self.change == True):
                # Który obiekt jest wybrany
                obj = context.active_object
                # Pobieramy dane obiekt
                oldmesh = obj.data
                # Pobieramy imie obiekta
                oldmeshname = obj.data.name
                 # Dodajemy element do obiekta
                obj.data = tuscan_column_mesh(self, context)
                # Próbujemy usunąś wszystkie grupy wierzchołek
                try:
                    bpy.ops.object.vertex_group_remove(all=True)
                except:
                    pass

                # Podlącamy materiji
                for material in oldmesh.materials:
                    obj.data.materials.append(material)

                # Usuwamy stary obiekt
                bpy.data.meshes.remove(oldmesh)
                # Przepisujemy imie
                obj.data.name = oldmeshname
            else:
                # Tworzymy kolumne 
                mesh = tuscan_column_mesh(self, context)
                # Tworzymy obiekt oraz przpisujemy dane 
                obj = object_utils.object_data_add(context, mesh, operator=self)

            obj.data["Tuscan Column"] = True
            obj.data["change"] = False
            # Pobieramy parametry
            for prm in TuscanColumnParameters():
                obj.data[prm] = getattr(self, prm)

        if bpy.context.mode == "EDIT_MESH":
            # Pobieramy z context aktywny obiekt
            active_object = context.active_object
            # Pobieramy jego imie
            name_active_object = active_object.name
            # Przechodzimy w tryb OBJECT
            bpy.ops.object.mode_set(mode='OBJECT')
            # Pobieramy nowego mesha
            mesh = tuscan_column_mesh(self, context)
            # Dodajemy obiekt
            obj = object_utils.object_data_add(context, mesh, operator=self)
            # Sprawdzamy czy jest wybrany obiekt
            obj.select_set(True)
            # Wybieramy obiekt
            active_object.select_set(True)
            # Dodajemy do wybranego stary obiekt
            bpy.context.view_layer.objects.active = active_object
            # Połączamy dwa obiekta 
            bpy.ops.object.join()
            # Przepisujemy imie nowemu obiektowi
            context.active_object.name = name_active_object
            #Przełącamy tryb w EDIT
            bpy.ops.object.mode_set(mode='EDIT')

        # Przechodzimy w Edit mode
        if use_enter_edit_mode:
            bpy.ops.object.mode_set(mode = 'EDIT')

        # restore pre operator state
        bpy.context.preferences.edit.use_enter_edit_mode = use_enter_edit_mode
        # Zwracamy że program jest zakończył się
        
        return {'FINISHED'}

# -------------------------- Collection Parameters  ------------------------- PROPERTY GROUPS

def TuscanColumnParameters():
    '''
        Funkcja zwacająca parametry
    '''
    TuscanColumnParameters = [
        "segments",
        "radius",
        "width",
        ]
    return TuscanColumnParameters
