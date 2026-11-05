from flask import Flask, render_template, request, url_for
import os, cv2, json, ezdxf
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def process_design(image_path, site_length, site_width, client_name, location):
    img = cv2.imread(image_path)
    if img is None:
        return None, None, None
        
    clean_img_path = os.path.join(app.config['OUTPUT_FOLDER'], 'clean_input.png')
    cv2.imwrite(clean_img_path, img)
    
    # 1. Image Processing (सुधारिएको)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
    
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # भित्री र बाहिरी दुवै पर्खाल पत्ता लगाउन RETR_TREE प्रयोग गर्ने
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    walls_data = []
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if 500 < area < 50000: # धेरै सानो (फोहोर) र धेरै ठूलो (बोर्डर) हटाउने
            x, y, w, h = cv2.boundingRect(cnt)
            # फोहोर हटाउन aspect ratio जाँच्ने
            if w > 10 and h > 10: 
                walls_data.append({"x": x, "y": y, "w": w, "h": h})

    pixel_to_feet = site_length / 800 
    
    # 2. AutoCAD DXF
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
    
    total_builtup_pixels = sum([w["w"] * w["h"] for w in walls_data])
    builtup_sqft = total_builtup_pixels * (pixel_to_feet**2)
    site_area_sqft = site_length * site_width
    far = builtup_sqft / site_area_sqft if site_area_sqft > 0 else 0
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 120, "1. AREA STATEMENT")
    c.setFont("Helvetica", 11)
    c.drawString(40, height - 140, f"Total Plot Area: {site_area_sqft:.2f} Sq. Ft.")
    c.drawString(40, height - 155, f"Total Built-up Area: {builtup_sqft:.2f} Sq. Ft.")
    c.drawString(40, height - 170, f"F.A.R. (Floor Area Ratio): {far:.2f}")

    c.save()

    # 4. Python 3D Render (सुधारिएको)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for w in walls_data:
        x = w['x'] * 0.05
        y = w['y'] * 0.05
        dx = w['w'] * 0.05
        dy = w['h'] * 0.05
        dz = 3.0 
        # पारदर्शी पर्खाल (alpha=0.3) ताकि भित्र देखियोस्
        ax.bar3d(x, y, 0, dx, dy, dz, color='skyblue', edgecolor='black', alpha=0.3)
        
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3D View - {client_name}')
    
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
            if not dxf:
                return "Error processing image. Please try another image.", 400
                
            return render_template('index.html', 
                                   dxf_url=url_for('static', filename='outputs/Municipal_Plan.dxf'),
                                   pdf_url=url_for('static', filename='outputs/Municipal_Report.pdf'),
                                   render_url=url_for('static', filename='outputs/3D_Render.png'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)