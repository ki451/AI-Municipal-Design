
import bpy
import math

# सफा स्क्रिन (Clear Scene)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

rooms = [{"name": "LIVING", "x": 0, "y": 0, "w": 6, "h": 8}, {"name": "FAMILY", "x": 0, "y": 8, "w": 6, "h": 8}, {"name": "BED 1", "x": 0, "y": 16, "w": 6, "h": 7}, {"name": "KITCHEN", "x": 0, "y": 23, "w": 6, "h": 7}, {"name": "STAIR", "x": 6, "y": 0, "w": 6, "h": 8}, {"name": "PUJA", "x": 6, "y": 8, "w": 3, "h": 8}, {"name": "BATH", "x": 9, "y": 8, "w": 3, "h": 8}, {"name": "BED 2", "x": 6, "y": 16, "w": 6, "h": 7}, {"name": "DINING", "x": 6, "y": 23, "w": 6, "h": 7}]

# सामग्री (Material)
mat_wall = bpy.data.materials.new(name="WallMat")
mat_wall.diffuse_color = (0.9, 0.9, 0.9, 1)
mat_floor = bpy.data.materials.new(name="FloorMat")
mat_floor.diffuse_color = (0.2, 0.2, 0.2, 1)

# भुइँ (Floor)
bpy.ops.mesh.primitive_plane_add(size=40, location=(6, 15, 0))
floor = bpy.context.active_object
floor.data.materials.append(mat_floor)

# कोठाहरूको 3D पर्खाल बनाउने
for r in rooms:
    x, y, w, h = r["x"], r["y"], r["w"], r["h"]
    # कोठाको बक्स
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + w/2, y + h/2, 1.5))
    cube = bpy.context.active_object
    cube.scale = (w, h, 3) # 3 मिटर उचाइ
    cube.data.materials.append(mat_wall)

# ३ तल्ला बनाउन माथि सार्ने (यहाँ सजिलोको लागि एउटा तल्ला मात्र बनाइएको छ)

# क्यामेरा राख्ने
bpy.ops.object.camera_add(location=(25, -15, 25), rotation=(math.radians(60), 0, math.radians(45)))
bpy.context.scene.camera = bpy.context.active_object

# उज्यालो (Light)
bpy.ops.object.light_add(type='SUN', location=(10, 10, 30))
bpy.context.active_object.data.energy = 5

# रेन्डर सेटिङ
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = r"C:\Users\Msi\AIBrain\designs\House_3D_Render.png"

# रेन्डर गर्ने
bpy.ops.render.render(write_still=True)
