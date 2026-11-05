from flask import Flask, render_template, request, url_for
import os, json, ezdxf, io, base64
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import google.generativeai as genai

app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'static', 'outputs')
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 🔒 API Key Render को Environment Variable बाट आउँछ
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_designs_from_ai(site_length, site_width, requirements):
    if not GEMINI_API_KEY:
        print("❌ API Key missing!")
        return get_fallback_designs(site_length, site_width)

    # 🧠 साँच्चिकैको इन्जिनियर दिमाग (Agentic Prompt)
    model = genai.GenerativeModel('gemini-1.5-pro') # Pro model is much smarter
    
    prompt = f"""
    You are the Chief Architect and Structural Engineer of Nepal. You strictly follow the Nepal National Building Code (NBC) and Vastu Shastra.
    Site Dimensions: {site_length} ft by {site_width} ft.
    Client Requirements: {requirements}.

    Before generating the layout, you MUST think step-by-step and apply these rules:
    1. SETBACKS: Leave 5 ft from the front, 3 ft from the back, and 3 ft from both sides. The buildable area is the remaining space.
    2. GROUND COVERAGE: Do not exceed 70% of the total site area.
    3. ROOM SIZES: Minimum room sizes must be respected (e.g., Bedroom >= 10x10 ft, Kitchen >= 8x8 ft). Do not overlap rooms.
    4. VASTU: Place Puja room in the North-East direction if requested.

    Generate exactly 5 DIFFERENT layout concepts (e.g., L-Shape, U-Shape, Vastu Friendly, Open Plan, Compact).
    
    Return the result STRICTLY as a valid JSON array of 5 objects. No markdown, no extra text.
    Format:
    [
      {{
        "title": "Concept Name",
        "rooms": [
          {{"name": "Living Room", "x": 5, "y": 5, "w": 15, "h": 12}}
        ],
        "boq": {{
          "cement_bags": 450,
          "steel_kg": 2500,
          "bricks": 8000,
          "sand_cft": 1200
        }},
        "estimated_cost_npr": 4500000
      }}
    ]
    Note: Calculate the BOQ and cost based on standard Nepali market rates and the total built-up area.
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json", "temperature": 0.7}
        )
        designs = json.loads(response.text)
        if len(designs) != 5:
            raise Exception("AI did not return exactly 5 designs")
        return designs
    except Exception as e:
        print("⚠️ Gemini Error, using fallback:", e)
        return get_fallback_designs(site_length, site_width)

def get_fallback_designs(site_length, site_width):
    # ... (Fallback logic remains the same, in case API fails)
    s_l = site_length - 10
    s_w = site_width - 10
    return [
        {"title": "Standard Plan (Fallback)", "rooms": [{"name": "Living", "x": 5, "y": 5, "w": s_l, "h": s_w/2}, {"name": "Kitchen", "x": 5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2}, {"name": "Bed", "x": s_l/2+5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2}], "boq": {}, "estimated_cost_npr": 0},
        {"title": "Open Plan (Fallback)", "rooms": [{"name": "Living+Kitchen", "x": 5, "y": 5, "w": s_l, "h": s_w*0.6}, {"name": "Bed 1", "x": 5, "y": s_w*0.6+5, "w": s_l/2, "h": s_w*0.4}, {"name": "Bed 2", "x": s_l/2+5, "y": s_w*0.6+5, "w": s_l/2, "h": s_w*0.4}], "boq": {}, "estimated_cost_npr": 0},
        {"title": "L-Shape House (Fallback)", "rooms": [{"name": "Living", "x": 5, "y": 5, "w": s_l, "h": s_w/2}, {"name": "Bed", "x": 5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2},{"name": "Kitchen", "x": s_l/2+5, "y": s_w/2+5, "w": s_l/2, "h": s_w/4}], "boq": {}, "estimated_cost_npr": 0},
        {"title": "U-Shape (Fallback)", "rooms": [{"name": "Bed 1", "x": 5, "y": 5, "w": s_l/3, "h": s_w}, {"name": "Living", "x": s_l/3+5, "y": 5, "w": s_l/3, "h": s_w*0.6},{"name": "Bed 2", "x": 2*s_l/3+5, "y": 5, "w": s_l/3, "h": s_w}], "boq": {}, "estimated_cost_npr": 0},
        {"title": "Vastu Friendly (Fallback)", "rooms": [{"name": "Puja", "x": 5, "y": s_w-10, "w": 10, "h": 10},{"name": "Living", "x": 5, "y": 5, "w": s_l, "h": s_w/2},{"name": "Kitchen", "x": s_l/2+5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2-15},{"name": "Bed", "x": 5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2-15}], "boq": {}, "estimated_cost_npr": 0}
    ]

@app.route('/', methods=['GET', 'POST'])
def index():
    designs_data = None
    if request.method == 'POST':
        site_length = float(request.form.get('site_length', 30))
        site_width = float(request.form.get('site_width', 40))
        client_name = request.form.get('client_name', 'Client')
        location = request.form.get('location', 'Kathmandu')
        requirements = request.form.get('requirements', '2 Bedrooms')
        
        ai_designs = get_designs_from_ai(site_length, site_width, requirements)
        designs_data = []

        for i, design in enumerate(ai_designs):
            rooms = design.get("rooms", [])
            title = design.get("title", f"Option {i+1}")
            boq = design.get("boq", {})
            est_cost = design.get("estimated_cost_npr", 0)
            
            # 1. AutoCAD DXF
            doc = ezdxf.new('R2010')
            msp = doc.modelspace()
            doc.layers.add(name="Walls", color=7)
            for r in rooms:
                points = [(r["x"], r["y"]), (r["x"]+r["w"], r["y"]), (r["x"]+r["w"], r["y"]+r["h"]), (r["x"], r["y"]+r["h"])]
                msp.add_lwpolyline(points, close=True, dxfattribs={"layer": "Walls"})
                msp.add_text(r["name"], dxfattribs={"layer": "Walls", "height": 1}).set_placement((r["x"]+2, r["y"]+2))
            
            dxf_filename = f"Plan_Option_{i+1}.dxf"
            dxf_path = os.path.join(app.config['OUTPUT_FOLDER'], dxf_filename)
            doc.saveas(dxf_path)

            # 2. PDF Report (With BOQ)
            pdf_filename = f"Report_Option_{i+1}.pdf"
            pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
            c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
            width, height = landscape(A4)
            c.setStrokeColor(colors.black)
            c.setLineWidth(2)
            c.rect(20, 20, width-40, height-40)
            
            c.setFont("Helvetica-Bold", 16)
            c.drawString(40, height - 60, f"MUNICIPAL BUILDING PERMIT - {title.upper()}")
            c.setFont("Helvetica", 12)
            c.drawString(40, height - 80, f"Client: {client_name} | Location: {location}")
            
            total_area = site_length * site_width
            builtup = sum([r["w"] * r["h"] for r in rooms])
            far = builtup / total_area if total_area > 0 else 0
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, height - 120, "1. AREA STATEMENT (Nepal Building Code)")
            c.setFont("Helvetica", 11)
            c.drawString(40, height - 140, f"Total Plot Area: {total_area:.2f} Sq. Ft.")
            c.drawString(40, height - 155, f"Total Built-up Area: {builtup:.2f} Sq. Ft.")
            c.drawString(40, height - 170, f"F.A.R.: {far:.2f}")
            c.drawString(40, height - 185, f"Ground Coverage: {(builtup/total_area)*100:.1f}% (Max 70%)")
            
            # BOQ Section
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, height - 230, "2. ESTIMATED MATERIALS (BOQ)")
            c.setFont("Helvetica", 11)
            c.drawString(40, height - 250, f"Cement: {boq.get('cement_bags', 'N/A')} Bags")
            c.drawString(40, height - 265, f"Steel: {boq.get('steel_kg', 'N/A')} Kg")
            c.drawString(40, height - 280, f"Bricks: {boq.get('bricks', 'N/A')} Pcs")
            c.drawString(40, height - 295, f"Estimated Cost: NPR {est_cost:,.2f}")
            
            c.save()

            # 3. Python 3D Render (Base64 Image)
            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111, projection='3d')
            colors_list = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0', '#ffb3e6']
            
            for j, r in enumerate(rooms):
                x, y, w, h = r['x'], r['y'], r['w'], r['h']
                color = colors_list[j % len(colors_list)]
                ax.add_collection3d(Poly3DCollection([[(x,y,0), (x+w,y,0), (x+w,y+h,0), (x,y+h,0)]], color=color, alpha=0.8))
                for z in [0, 3]:
                    ax.plot([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], [z, z, z, z, z], color='black', linewidth=1)
                ax.plot([x, x], [y, y], [0, 3], color='black', linewidth=1)
                ax.plot([x+w, x+w], [y, y], [0, 3], color='black', linewidth=1)
                ax.plot([x, x], [y+h, y+h], [0, 3], color='black', linewidth=1)
                ax.plot([x+w, x+w], [y+h, y+h], [0, 3], color='black', linewidth=1)

            ax.set_xlim(0, site_length)
            ax.set_ylim(0, site_width)
            ax.set_zlim(0, 4)
            ax.set_title(title)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close(fig)
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')

            designs_data.append({
                "title": title,
                "dxf_url": url_for('static', filename=f'outputs/{dxf_filename}'),
                "pdf_url": url_for('static', filename=f'outputs/{pdf_filename}'),
                "render_base64": img_base64,
                "boq": boq,
                "est_cost": est_cost
            })

    return render_template('index.html', designs=designs_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)