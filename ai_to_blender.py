import cv2
import numpy as np
import json
import subprocess
import os
import tkinter as tk
from tkinter import filedialog
import ezdxf
from fpdf import FPDF

def generate_municipal_package():
    print("🏛️ 1. नगरपालिका डिजाइन प्याकेज सुरु गर्दै...")
    
    # फोटो सेलेक्ट गर्ने
    root = tk.Tk()
    root.withdraw()
    print("📂 कृपया आफ्नो 2D Floor Plan फोटो सेलेक्ट गर्नुहोस्...")
    image_path = filedialog.askopenfilename(title="Select Floor Plan", filetypes=[("Image files", "*.jpg *.png")])
    
    if not image_path: return
    img = cv2.imread(image_path)
    
    # 2D प्रोसेसिङ
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    walls_data = []
    preview_img = img.copy()
    
    # पर्खाल फिल्टर गर्ने
    for cnt in contours:
        if cv2.contourArea(cnt) > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            walls_data.append({"x": x, "y": y, "w": w, "h": h})
            cv2.rectangle(preview_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    out_dir = r"C:\Users\Msi\AIBrain\designs"
    os.makedirs(out_dir, exist_ok=True)
    cv2.imwrite(os.path.join(out_dir, "2D_Plan.png"), preview_img)

    # --- 1. AutoCAD (DXF) फाइल बनाउने (नगरपालिकाको लागि) ---
    print("📐 2. AutoCAD (DXF) नक्सा बनाउँदै...")
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    for w in walls_data:
        # AutoCAD मा पर्खाल (Rectangle) कोरा
        msp.add_lwpolyline([
            (w["x"], w["y"]), 
            (w["x"] + w["w"], w["y"]), 
            (w["x"] + w["w"], w["y"] + w["h"]), 
            (w["x"], w["y"] + w["h"])
        ], close=True)
    dxf_path = os.path.join(out_dir, "Municipal_Floor_Plan.dxf")
    doc.saveas(dxf_path)
    print(f"✅ DXF नक्सा तयार: {dxf_path}")

    # --- 2. Area Statement (PDF) बनाउने ---
    print("📄 3. Area Statement (PDF) बनाउँदै...")
    total_area_pixels = sum([w["w"] * w["h"] for w in walls_data])
    # मानौं 1 pixel = 0.05 meter
    scale = 0.05 
    total_area_sqm = (total_area_pixels * (scale**2)) / 2 # अनुमानित क्षेत्रफल
    total_area_sqft = total_area_sqm * 10.7639

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="MUNICIPAL BUILDING PERMIT - AREA STATEMENT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Total Built-up Area: {total_area_sqm:.2f} Sq. Meters", ln=True)
    pdf.cell(200, 10, txt=f"Total Built-up Area: {total_area_sqft:.2f} Sq. Feet", ln=True)
    pdf.cell(200, 10, txt=f"Total Walls Detected: {len(walls_data)}", ln=True)
    pdf.cell(200, 10, txt="Note: This is an AI-generated draft. Requires Engineer's Signature.", ln=True)
    pdf_path = os.path.join(out_dir, "Area_Statement.pdf")
    pdf.output(pdf_path)
    print(f"✅ Area Statement तयार: {pdf_path}")

    # --- 3. Blender कोड जेनेरेट गर्ने ---
    print("📝 4. 3D Blender कोड तयार गर्दै...")
    json_path = os.path.join(out_dir, "walls_data.json")
    with open(json_path, "w") as f:
        json.dump(walls_data, f)

    blender_script_path = os.path.join(out_dir, "blender_advanced.py")
    blender_code = f"""
import bpy, json, math

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

with open(r"{json_path}", "r") as f:
    walls = json.load(f)

# जमिन
bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 0, 0))
floor = bpy.context.active_object
mat_f = bpy.data.materials.new(name="Floor"); mat_f.use_nodes=True
mat_f.node_tree.nodes["Principled BSDF"].inputs[0].default_value=(0.2,0.1,0.05,1)
floor.data.materials.append(mat_f)

# पर्खाल
for w in walls:
    x3d = (w["x"] - 400) * 0.05
    y3d = -(w["y"] - 300) * 0.05
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x3d, y3d, 1.5))
    wall = bpy.context.active_object
    wall.scale = (w["w"] * 0.05, w["h"] * 0.05, 1.5)
    mat_w = bpy.data.materials.new(name="Wall"); mat_w.use_nodes=True
    mat_w.node_tree.nodes["Principled BSDF"].inputs[0].default_value=(0.9,0.9,0.9,1)
    wall.data.materials.append(mat_w)

# क्यामेरा र लाइट
bpy.ops.object.camera_add(location=(15, -15, 15), rotation=(math.radians(60), 0, math.radians(45)))
bpy.context.scene.camera = bpy.context.active_object
bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
bpy.context.active_object.data.energy = 5

bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.filepath = r"{os.path.join(out_dir, 'Municipal_3D_Render.png')}"
bpy.ops.render.render(write_still=True)
"""
    with open(blender_script_path, "w") as f: f.write(blender_code)

    # --- 4. Blender चलाउने ---
    print("🚀 5. Blender मा 3D रेन्डर गर्दै...")
    blender_exe = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" # तपाईंको भर्सन अनुसार
    
    try:
        subprocess.run([blender_exe, "-b", "-P", blender_script_path], check=True)
        print("\n🎉 सफल! नगरपालिकाको लागि पूरा प्याकेज तयार भयो।")
        print(f"📁 फाइलहरू यहाँ छन्: {out_dir}")
        os.startfile(out_dir) # फोल्डर खोल्ने
    except Exception as e:
        print(f"❌ Blender एरर: {e}")

if __name__ == "__main__":
    generate_municipal_package()