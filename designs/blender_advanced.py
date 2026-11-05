
import bpy
import math
import json

# सफा स्क्रिन
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

rooms = [{"name": "LIVING", "x": 0, "y": 0, "w": 6, "h": 8}, {"name": "FAMILY", "x": 0, "y": 8, "w": 6, "h": 8}, {"name": "BED 1", "x": 0, "y": 16, "w": 6, "h": 7}, {"name": "KITCHEN", "x": 0, "y": 23, "w": 6, "h": 7}, {"name": "STAIR", "x": 6, "y": 0, "w": 6, "h": 8}, {"name": "PUJA", "x": 6, "y": 8, "w": 3, "h": 8}, {"name": "BATH", "x": 9, "y": 8, "w": 3, "h": 8}, {"name": "BED 2", "x": 6, "y": 16, "w": 6, "h": 7}, {"name": "DINING", "x": 6, "y": 23, "w": 6, "h": 7}]

# सामग्रीहरू (Materials)
mat_wall = bpy.data.materials.new(name="Wall_White")
mat_wall.use_nodes = True
mat_wall.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1)

mat_floor = bpy.data.materials.new(name="Floor_Wood")
mat_floor.use_nodes = True
mat_floor.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.4, 0.2, 0.1, 1)

# झ्यालको लागि निलो रङ (Transmission को झन्झट बिना)
mat_glass = bpy.data.materials.new(name="Glass_Blue")
mat_glass.use_nodes = True
mat_glass.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.4, 0.8, 1)

# भुइँ (Floor)
bpy.ops.mesh.primitive_plane_add(size=40, location=(6, 15, 0))
floor = bpy.context.active_object
floor.data.materials.append(mat_floor)

wall_height = 3.0

# पर्खाल र झ्यालहरू बनाउने
for r in rooms:
    x, y, w, h = r["x"], r["y"], r["w"], r["h"]
    
    # पर्खाल
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + w/2, y + h/2, wall_height/2))
    cube = bpy.context.active_object
    cube.scale = (w, h, wall_height)
    cube.data.materials.append(mat_wall)
    
    # झ्याल
    if r["name"] not in ["STAIR", "BATH"]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x + w/2, y, wall_height/2 + 0.5))
        win = bpy.context.active_object
        win.scale = (w/2, 0.1, 1.2)
        win.data.materials.append(mat_glass)

# छाना (Roof)
bpy.ops.mesh.primitive_cube_add(size=1, location=(6, 15, wall_height + 0.2))
roof = bpy.context.active_object
roof.scale = (12.5, 30.5, 0.4)
roof.data.materials.append(mat_wall)

# क्यामेरा (Camera)
bpy.ops.object.camera_add(location=(25, -20, 20), rotation=(math.radians(65), 0, math.radians(45)))
bpy.context.scene.camera = bpy.context.active_object

# उज्यालो (Sun)
bpy.ops.object.light_add(type='SUN', location=(10, 10, 30))
sun = bpy.context.active_object
sun.data.energy = 3.0
sun.rotation_euler = (math.radians(45), math.radians(45), 0)

# रेन्डर सेटिङ
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = r"C:\Users\Msi\AIBrain\designs\Advanced_House_3D_Render.png"

# रेन्डर गर्ने
bpy.ops.render.render(write_still=True)
