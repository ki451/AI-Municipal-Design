from flask import Flask, render_template, request, url_for
import os, json, ezdxf
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = 'static/outputs'
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

#⚠️ यहाँ तपाईंको Google Gemini API Key राख्नुहोला
GEMINI_API_KEY = "AQ.Ab8RN6IT9ZxCz9Pk81gBEDgidlRONeT4G7U4-..." # तपाईंको Key यहाँ राख्नुहोला
genai.configure(api_key=GEMINI_API_KEY)

def generate_design(site_length, site_width, requirements):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert architect. Design a house for a site of {site_length}x{site_width} feet.
    Requirements: {requirements}.
    
    Return ONLY a valid JSON array of rooms. 
    Each room must have: "name" (string), "x" (number), "y" (number), "w" (number), "h" (number).
    All dimensions must be in feet.
    Ensure rooms DO NOT overlap and fit within the site dimensions.
    Use the bottom-left corner as (0,0).
    Do not include markdown, only the JSON array.
    Example: [{{"name": "Living", "x": 0, "y": 0, "w": 15, "h": 12}}]
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        rooms = json.loads(text)
        if not rooms:
            raise Exception("Empty design")
        return rooms
    except Exception as e:
        print("Gemini Error:", e)
        # Fallback simple design
        return [
            {"name": "Living", "x": 0, "y": 0, "w": site_length*0.6, "h": site_width*0.4},
            {"name": "Kitchen", "x": site_length*0.6, "y": 0, "w": site_length*0.4, "h": site_width*0.4},
            {"name": "Bed 1", "x": 0, "y": site_width*0.4, "w": site_length*0.5, "h": site_width*0.6},
            {"name": "Bed 2", "x": site_length*0.5, "y": site_width*0.4, "w": site_length*0.5, "h": site_width*0.6}
        ]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        site_length = float(request.form.get('site_length', 30))
        site_width = float(request.form.get('site_width', 40))
        client_name = request.form.get('client_name', 'Client')
        location = request.form.get('location', 'Kathmandu')
        requirements = request.form.get('requirements', '2 Bedrooms, 1 Kitchen')
        
        rooms = generate_design(site_length, site_width, requirements)

        # --- 1. AutoCAD DXF ---
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        doc.layers.add(name="Walls", color=7)
        for r in rooms:
            points = [(r["x"], r["y"]), (r["x"]+r["w"], r["y"]), (r["x"]+r["w"], r["y"]+r["h"]), (r["x"], r["y"]+r["h"])]
            msp.add_lwpolyline(points, close=True, dxfattribs={"layer": "Walls"})
            msp.add_text(r["name"], dxfattribs={"layer": "Walls", "height": 1}).set_placement((r["x"]+1, r["y"]+1))
        
        dxf_path = os.path.join(app.config['OUTPUT_FOLDER'], "Municipal_Plan.dxf")
        doc.saveas(dxf_path)

        # --- 2. PDF Report ---
        pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], "Municipal_Report.pdf")
        c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
        width, height = landscape(A4)
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(20, 20, width-40, height-40)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(40, height - 60, "MUNICIPAL BUILDING PERMIT - MASTER REPORT")
        c.setFont("Helvetica", 12)
        c.drawString(40, height - 80, f"Client: {client_name} | Location: {location}")
        
        total_area = site_length * site_width
        builtup = sum([r["w"] * r["h"] for r in rooms])
        far = builtup / total_area if total_area > 0 else 0
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, height - 120, "1. AREA STATEMENT")
        c.setFont("Helvetica", 11)
        c.drawString(40, height - 140, f"Total Plot Area: {total_area:.2f} Sq. Ft.")
        c.drawString(40, height - 155, f"Total Built-up Area: {builtup:.2f} Sq. Ft.")
        c.drawString(40, height - 170, f"F.A.R. (Floor Area Ratio): {far:.2f}")
        
        c.save()

        # --- 3. Python 3D Render (Wireframe style) ---
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        for r in rooms:
            x, y, w, h = r['x'], r['y'], r['w'], r['h']
            # Floor
            ax.plot3D([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], [0, 0, 0, 0, 0], color='gray')
            
            # Walls (Lines)
            # Front
            ax.plot3D([x, x+w], [y, y], [0, 3], color='black')
            # Back
            ax.plot3D([x, x+w], [y+h, y+h], [0, 3], color='black')
            # Left
            ax.plot3D([x, x], [y, y+h], [0, 3], color='black')
            # Right
            ax.plot3D([x+w, x+w], [y, y+h], [0, 3], color='black')
            
            # Top (Roof outline)
            ax.plot3D([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], [3, 3, 3, 3, 3], color='blue')

        ax.set_xlim(0, site_length)
        ax.set_ylim(0, site_width)
        ax.set_zlim(0, 4)
        ax.set_xlabel('Length (ft)')
        ax.set_ylabel('Width (ft)')
        ax.set_zlabel('Height (ft)')
        ax.set_title(f'3D Floor Plan - {client_name}')
        
        render_path = os.path.join(app.config['OUTPUT_FOLDER'], '3D_Render.png')
        plt.savefig(render_path, dpi=150, bbox_inches='tight')
        plt.close()

        return render_template('index.html', 
                               dxf_url=url_for('static', filename='outputs/Municipal_Plan.dxf'),
                               pdf_url=url_for('static', filename='outputs/Municipal_Report.pdf'),
                               render_url=url_for('static', filename='outputs/3D_Render.png'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)