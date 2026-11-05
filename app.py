from flask import Flask, render_template, request, url_for
import os, json, ezdxf
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

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert licensed architect in Nepal. 
    Design exactly 5 different layout options for a house on a site of {site_length} ft by {site_width} ft.
    Client Requirements: {requirements}.
    
    Rules to follow strictly (Nepal Building Code):
    1. Leave a setback of at least 5 ft from the front, and 3 ft from sides/back.
    2. Do not exceed Ground Coverage of 70%.
    3. Include a Puja room in the North-East (Vastu).
    4. Ensure rooms do not overlap and fit within the buildable area.
    
    Return ONLY a valid JSON array of 5 objects. No markdown, no explanations.
    Format:
    [
      {{
        "title": "Name of Concept",
        "rooms": [
          {{"name": "Living", "x": 5, "y": 5, "w": 15, "h": 12}}
        ]
      }}
    ]
    All dimensions must be in feet. Use bottom-left corner as (0,0).
    """
    
    try:
        # response_mime_type ले JSON मात्र दिन बाध्य पार्छ
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        designs = json.loads(response.text)
        if len(designs) != 5:
            raise Exception("AI did not return exactly 5 designs")
        return designs
    except Exception as e:
        print("⚠️ Gemini Error, using fallback:", e)
        return get_fallback_designs(site_length, site_width)

def get_fallback_designs(site_length, site_width):
    # ५ वटा फरक-फरक ब्याकअप डिजाइन (यदि API फेल भयो भने)
    s_l = site_length - 10
    s_w = site_width - 10
    return [
        {"title": "Standard Plan (Fallback)", "rooms": [
            {"name": "Living", "x": 5, "y": 5, "w": s_l, "h": s_w/2}, 
            {"name": "Kitchen", "x": 5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2}, 
            {"name": "Bed", "x": s_l/2+5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2}
        ]},
        {"title": "Open Plan (Fallback)", "rooms": [
            {"name": "Living+Kitchen", "x": 5, "y": 5, "w": s_l, "h": s_w*0.6}, 
            {"name": "Bed 1", "x": 5, "y": s_w*0.6+5, "w": s_l/2, "h": s_w*0.4}, 
            {"name": "Bed 2", "x": s_l/2+5, "y": s_w*0.6+5, "w": s_l/2, "h": s_w*0.4}
        ]},
        {"title": "L-Shape House (Fallback)", "rooms": [
            {"name": "Living", "x": 5, "y": 5, "w": s_l, "h": s_w/2}, 
            {"name": "Bed", "x": 5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2},
            {"name": "Kitchen", "x": s_l/2+5, "y": s_w/2+5, "w": s_l/2, "h": s_w/4}
        ]},
        {"title": "U-Shape (Fallback)", "rooms": [
            {"name": "Bed 1", "x": 5, "y": 5, "w": s_l/3, "h": s_w}, 
            {"name": "Living", "x": s_l/3+5, "y": 5, "w": s_l/3, "h": s_w*0.6},
            {"name": "Bed 2", "x": 2*s_l/3+5, "y": 5, "w": s_l/3, "h": s_w}
        ]},
        {"title": "Vastu Friendly (Fallback)", "rooms": [
            {"name": "Puja", "x": 5, "y": s_w-10, "w": 10, "h": 10},
            {"name": "Living", "x": 5, "y": 5, "w": s_l, "h": s_w/2},
            {"name": "Kitchen", "x": s_l/2+5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2-15},
            {"name": "Bed", "x": 5, "y": s_w/2+5, "w": s_l/2, "h": s_w/2-15}
        ]}
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
            rooms = design["rooms"]
            title = design.get("title", f"Option {i+1}")
            
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

            # 2. PDF Report
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
            c.save()

            # 3. Python 3D Render (Wireframe)
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
            
            render_filename = f"Render_Option_{i+1}.png"
            render_path = os.path.join(app.config['OUTPUT_FOLDER'], render_filename)
            plt.savefig(render_path, dpi=100, bbox_inches='tight')
            plt.close()

            designs_data.append({
                "title": title,
                "dxf_url": url_for('static', filename=f'outputs/{dxf_filename}'),
                "pdf_url": url_for('static', filename=f'outputs/{pdf_filename}'),
                "render_url": url_for('static', filename=f'outputs/{render_filename}')
            })

    return render_template('index.html', designs=designs_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)