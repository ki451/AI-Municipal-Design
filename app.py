from flask import Flask, render_template, request, url_for
import os, cv2, json, subprocess, ezdxf
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

def process_design(image_path, site_length, site_width, client_name, location):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
    
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    walls_data = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 2000:
            x, y, w, h = cv2.boundingRect(cnt)
            walls_data.append({"x": x, "y": y, "w": w, "h": h})

    # स्केल क्याल्कुलेसन
    pixel_to_feet = site_length / 800 
    
    # --- 1. AutoCAD DXF ---
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    doc.layers.add(name="Walls", color=7)
    for w in walls_data:
        points = [(w["x"]*pixel_to_feet, w["y"]*pixel_to_feet), 
                  ((w["x"]+w["w"])*pixel_to_feet, w["y"]*pixel_to_feet), 
                  ((w["x"]+w["w"])*pixel_to_feet, (w["y"]+w["h"])*pixel_to_feet), 
                  (w["x"]*pixel_to_feet, (w["y"]+w["h"])*pixel_to_feet)]
        msp.add_lwpolyline(points, close=True, dxfattribs={"layer": "Walls"})
    
    dxf_path = os.path.join(app.config['OUTPUT_FOLDER'], "Municipal_Plan.dxf")
    doc.saveas(dxf_path)

    # --- 2. Calculations (Area & BOQ) ---
    total_builtup_pixels = sum([w["w"] * w["h"] for w in walls_data])
    builtup_sqft = total_builtup_pixels * (pixel_to_feet**2)
    site_area_sqft = site_length * site_width
    far = builtup_sqft / site_area_sqft if site_area_sqft > 0 else 0
    
    # Structural BOQ (Thumb rule calculation)
    cement_bags = int(builtup_sqft * 0.4)
    steel_kg = int(builtup_sqft * 4)
    sand_cft = int(builtup_sqft * 1.8)
    aggregate_cft = int(builtup_sqft * 1.35)
    bricks = int(builtup_sqft * 8)

    # --- 3. PDF Report (Area + BOQ) ---
    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], "Municipal_Report.pdf")
    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Border
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.rect(20, 20, width-40, height-40)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 60, "MUNICIPAL BUILDING PERMIT - MASTER REPORT")
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 80, f"Client: {client_name} | Location: {location}")
    
    # Area Table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 120, "1. AREA STATEMENT")
    c.setFont("Helvetica", 11)
    c.drawString(40, height - 140, f"Total Plot Area: {site_area_sqft:.2f} Sq. Ft.")
    c.drawString(40, height - 155, f"Total Built-up Area: {builtup_sqft:.2f} Sq. Ft.")
    c.drawString(40, height - 170, f"F.A.R. (Floor Area Ratio): {far:.2f}")

    # BOQ Table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 210, "2. ESTIMATED MATERIALS (BOQ)")
    c.setFont("Helvetica", 11)
    c.drawString(40, height - 230, f"Cement: {cement_bags} Bags")
    c.drawString(40, height - 245, f"Steel (Rebar): {steel_kg} Kg")
    c.drawString(40, height - 260, f"Sand: {sand_cft} Cft")
    c.drawString(40, height - 275, f"Aggregate: {aggregate_cft} Cft")
    c.drawString(40, height - 290, f"Bricks: {bricks} Pcs")
    
    c.drawString(40, height - 330, "*Note: These are estimated quantities. Actual may vary based on structural design.")
    
    c.drawImage(image_path, 450, 100, width=300, height=250, preserveAspectRatio=True)
    c.save()

    # --- 4. Blender 3D Render ---
    json_path = os.path.join(app.config['OUTPUT_FOLDER'], "walls.json")
    with open(json_path, "w") as f: json.dump(walls_data, f)

    blender_script = os.path.join(app.config['OUTPUT_FOLDER'], "render.py")
    b_code = f"""
import bpy, json, math
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
with open(r"{json_path}", "r") as f: walls = json.load(f)

bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 0, 0))
for w in walls:
    bpy.ops.mesh.primitive_cube_add(size=1, location=((w["x"]-400)*0.05, -(w["y"]-300)*0.05, 1.5))
    bpy.context.active_object.scale = (w["w"]*0.05, w["h"]*0.05, 1.5)
    mat = bpy.data.materials.new(name="Wall"); mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 1)
    bpy.context.active_object.data.materials.append(mat)

bpy.ops.object.camera_add(location=(0, -20, 20), rotation=(math.radians(45), 0, 0))
bpy.context.scene.camera = bpy.context.active_object
bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.filepath = r"{os.path.join(app.config['OUTPUT_FOLDER'], '3D_Render.png')}"
bpy.ops.render.render(write_still=True)
"""
    with open(blender_script, "w") as f: f.write(b_code)

    blender_exe = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
    try:
        subprocess.run([blender_exe, "-b", "-P", blender_script], check=True)
    except Exception as e:
        print("Blender Error:", e)

    return dxf_path, pdf_path, os.path.join(app.config['OUTPUT_FOLDER'], '3D_Render.png')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['floor_plan']
        site_length = float(request.form.get('site_length', 30))
        site_width = float(request.form.get('site_width', 40))
        client_name = request.form.get('client_name', 'Client')
        location = request.form.get('location', 'Kathmandu')
        
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            dxf, pdf, render = process_design(filepath, site_length, site_width, client_name, location)
            return render_template('index.html', 
                                   dxf_url=url_for('static', filename='outputs/Municipal_Plan.dxf'),
                                   pdf_url=url_for('static', filename='outputs/Municipal_Report.pdf'),
                                   render_url=url_for('static', filename='outputs/3D_Render.png'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
