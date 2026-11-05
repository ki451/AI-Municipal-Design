import os
import ezdxf
from ezdxf import colors
import math

def generate_3d_and_2d_engine():
    print("🧠 AI Engine: डिजाइन डेटा प्रोसेस गर्दै...")
    
    # १. AI ले दिएको डिजाइन डेटा (उदाहरण: १२x३० को घर)
    rooms = [
        {"name": "LIVING", "x": 0, "y": 0, "w": 6, "h": 8},
        {"name": "FAMILY", "x": 0, "y": 8, "w": 6, "h": 8},
        {"name": "BED 1", "x": 0, "y": 16, "w": 6, "h": 7},
        {"name": "KITCHEN", "x": 0, "y": 23, "w": 6, "h": 7},
        {"name": "STAIR", "x": 6, "y": 0, "w": 6, "h": 8},
        {"name": "PUJA", "x": 6, "y": 8, "w": 3, "h": 8},
        {"name": "BATH", "x": 9, "y": 8, "w": 3, "h": 8},
        {"name": "BED 2", "x": 6, "y": 16, "w": 6, "h": 7},
        {"name": "DINING", "x": 6, "y": 23, "w": 6, "h": 7}
    ]
    
    out_dir = r"C:\Users\Msi\AIBrain\designs"
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    # ==========================================
    # भाग १: 3D मोडेल जनरेट गर्ने (.obj) - Blender को लागि
    # ==========================================
    print("🏗️ 3D मोडेल (OBJ) बन्दै...")
    wall_height = 3.0 # Floor Height
    floors = 3       # 3 Floors

    obj_vertices = []
    obj_faces = []
    
    def add_v(x, y, z):
        obj_vertices.append((x, y, z))
        return len(obj_vertices)
        
    def add_f(v1, v2, v3, v4):
        obj_faces.append((v1, v2, v3, v4))

    for f in range(floors):
        z1 = f * wall_height
        z2 = (f + 1) * wall_height
        
        for r in rooms:
            x, y, w, h = r["x"], r["y"], r["w"], r["h"]
            # कोठाको 3D बक्स बनाउने
            v1 = add_v(x, y, z1)
            v2 = add_v(x+w, y, z1)
            v3 = add_v(x+w, y+h, z1)
            v4 = add_v(x, y+h, z1)
            v5 = add_v(x, y, z2)
            v6 = add_v(x+w, y, z2)
            v7 = add_v(x+w, y+h, z2)
            v8 = add_v(x, y+h, z2)
            
            add_f(v1, v2, v3, v4) # Bottom
            add_f(v5, v6, v7, v8) # Top
            add_f(v1, v2, v6, v5) # Front
            add_f(v2, v3, v7, v6) # Right
            add_f(v3, v4, v8, v7) # Back
            add_f(v4, v1, v5, v8) # Left

    obj_path = os.path.join(out_dir, "Kishan_AI_House_3D.obj")
    with open(obj_path, 'w') as f:
        for v in obj_vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in obj_faces:
            f.write(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")

    # ==========================================
    # भाग २: CAD फाइल जनरेट गर्ने (.dxf) - AutoCAD को लागि
    # ==========================================
    print("📐 2D CAD (DXF) बन्दै...")
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # लेयरहरू
    doc.layers.add('WALLS', color=colors.WHITE)
    doc.layers.add('DOORS', color=colors.MAGENTA)
    doc.layers.add('WINDOWS', color=colors.CYAN)
    doc.layers.add('TEXT', color=colors.YELLOW)

    # पर्खाल र कोठाको नाम कोर्ने
    for r in rooms:
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        # पर्खाल
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 35})
        # नाम
        msp.add_text(r["name"], dxfattribs={'layer': 'TEXT', 'height': 0.4}).set_placement((x + w/2, y + h/2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # ढोका (Arc)
    msp.add_arc((3, 8), radius=0.9, start_angle=180, end_angle=270, dxfattribs={'layer': 'DOORS'})
    msp.add_line((3, 8), (2.1, 8), dxfattribs={'layer': 'DOORS'})
    
    # झ्याल (Lines)
    msp.add_line((2, 0), (4, 0), dxfattribs={'layer': 'WINDOWS', 'lineweight': 40})
    
    # नाप (Dimensions)
    msp.add_linear_dim(base=(0, -2), p1=(0, 0), p2=(12, 0), dxfattribs={'layer': 'TEXT'}).render()
    msp.add_linear_dim(base=(-2, 0), p1=(0, 0), p2=(0, 30), angle=90, dxfattribs={'layer': 'TEXT'}).render()

    dxf_path = os.path.join(out_dir, "Kishan_AI_House_2D.dxf")
    doc.saveas(dxf_path)

    print(f"\n🎉 सफल! फाइलहरू तयार भए:")
    print(f"  - 3D Model: {obj_path} (यसलाई Blender वा 3D Viewer मा खोल्नुस्)")
    print(f"  - CAD File: {dxf_path} (यसलाई AutoCAD मा खोल्नुस्)")
    
    os.startfile(out_dir)

if __name__ == "__main__":
    generate_3d_and_2d_engine()
