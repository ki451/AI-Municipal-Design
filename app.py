from flask import Flask, render_template, request, url_for
import os, cv2, json, ezdxf
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# ⚠️ यहाँ तपाईंको नयाँ Google API Key राख्नुहोला
GEMINI_API_KEY = "YOUR_NEW_GEMINI_API_KEY_HERE" 
genai.configure(api_key=GEMINI_API_KEY)

def process_design(image_path, site_length, site_width, client_name, location):
    # 1. Google Gemini Vision API बाट डिजाइन मगाउने
    try:
        img = Image.open(image_path)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        You are an expert architect. Analyze this 2D floor plan image.
        Return ONLY a valid JSON array of rooms. 
        Each room must have: "name" (string), "x" (int), "y" (int), "w" (int), "h" (int).
        Use a 0-1000 scale for coordinates. 
        Do not include markdown, only the JSON array.
        Example: [{"name": "Living Room", "x": 0, "y": 0, "w": 500, "h": 400}]
        """
        
        response = model.generate_content([prompt, img])
        text = response.text.replace("```json", "").replace("```", "").strip()
        walls_data = json.loads(text)
        
        # यदि AI ले खाली डाटा दियो भने, पुरानो OpenCV तरिका अपनाउने (Fallback)
        if not walls_data:
            raise Exception("AI returned empty")

    except Exception as e:
        print("Gemini API Error, using OpenCV fallback:", e)
        # Fallback: OpenCV
        img_cv = cv2.imread(image_path)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        walls_data = []
        for cnt in contours:
            if 1000 < cv2.contourArea(cnt) < 100000:
                x, y, w, h = cv2.boundingRect(cnt)
                walls_data.append({"name": "Room", "x": x, "y": y, "w": w, "h": h})

    # 2. AutoCAD DXF
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    doc.layers.add(name="Walls", color=7)
    for w in walls_data:
        points = [(w["x"], w["y"]), 
                  (w["x"]+w["w"], w["y"]), 
                  (w["x"]+w["w"], w["y"]+w["h"]), 
                  (w["x"], w["y"]+w["h"])]
        msp.add_lwpolyline(points, close=True, dxfattribs={"layer": "Walls"})
        if "name" in w:
            msp.add_text(w["name"], dxfattribs={"layer": "Walls"}).set_placement((w["x"], w["y"]+5))
    
    dxf_path = os.path.join(app.config['OUTPUT_FOLDER'], "Municipal_Plan.dxf")
    doc.saveas(dxf_path)

    # 3. PDF Report
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
    
    total_builtup = sum([w["w"] * w["h"] for w in walls_data])
    site_area = site_length * site_width
    far = total_builtup / site_area if site_area > 0 else 0
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 120, "1. AREA STATEMENT")
    c.setFont("Helvetica", 11)
    c.drawString(40, height - 140, f"Total Plot Area: {site_area:.2f} Sq. Ft.")
    c.drawString(40, height - 155, f"Total Built-up Area: {total_builtup:.2f} Sq. Ft.")
    c.drawString(40, height - 170, f"F.A.R. (Floor Area Ratio): {far:.2f}")
    
    c.save()

    # 4. Python 3D Render (Rooms with Walls)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    for w in walls_data:
        x = w['x'] * 0.1
        y = w['y'] * 0.1
        dx = w['w'] * 0.1
        dy = w['h'] * 0.1
        dz = 3.0 
        # पर्खाल (बक्स)
        ax.bar3d(x, y, 0, dx, dy, dz, color='#87CEEB', edgecolor='black', alpha=0.6)
        
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3D AI Architect View - {client_name}')
    
    render_path = os.path.join(app.config['OUTPUT_FOLDER'], '3D_Render.png')
    plt.savefig(render_path, dpi=150, bbox_inches='tight')
    plt.close()

    return dxf_path, pdf_path, render_path

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