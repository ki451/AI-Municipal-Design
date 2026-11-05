from flask import Flask, render_template, request, url_for
import os, json, ezdxf, io, base64
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'static', 'outputs')
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# 🧠 KISHAN AI - RULE BASED EXPERT ENGINE (No API Key Required)
def generate_kishan_ai_designs(site_length, site_width, requirements):
    # १. नेपाल सरकारको नियम अनुसार सेटब्याक (Setback) निकाल्ने (Front 5ft, Sides 3ft)
    buildable_length = site_length - (5 + 3) # 5ft front, 3ft back
    buildable_width = site_width - (3 + 3)   # 3ft left, 3ft right
    
    if buildable_length <= 0 or buildable_width <= 0:
        buildable_length = site_length * 0.8
        buildable_width = site_width * 0.8

    # २. ५ वटा फरक-फरक डिजाइनको लजिक (Space Planning)
    designs = []
    
    # Option 1: Standard Plan (Living front, Beds back)
    d1_rooms = [
        {"name": "Living", "x": 3, "y": 3, "w": buildable_width, "h": buildable_length * 0.4},
        {"name": "Kitchen", "x": 3, "y": 3 + buildable_length * 0.4, "w": buildable_width * 0.4, "h": buildable_length * 0.6},
        {"name": "Bed 1", "x": 3 + buildable_width * 0.4, "y": 3 + buildable_length * 0.4, "w": buildable_width * 0.6, "h": buildable_length * 0.3},
        {"name": "Bed 2", "x": 3 + buildable_width * 0.4, "y": 3 + buildable_length * 0.7, "w": buildable_width * 0.6, "h": buildable_length * 0.3}
    ]
    designs.append({"title": "Standard Plan (Kishan AI)", "rooms": d1_rooms})

    # Option 2: Vastu Friendly (Puja in North-East)
    d2_rooms = [
        {"name": "Living", "x": 3, "y": 3, "w": buildable_width, "h": buildable_length * 0.5},
        {"name": "Kitchen", "x": 3, "y": 3 + buildable_length * 0.5, "w": buildable_width * 0.5, "h": buildable_length * 0.5},
        {"name": "Bed", "x": 3 + buildable_width * 0.5, "y": 3 + buildable_length * 0.5, "w": buildable_width * 0.3, "h": buildable_length * 0.5},
        {"name": "Puja", "x": 3 + buildable_width * 0.8, "y": 3 + buildable_length * 0.8, "w": buildable_width * 0.2, "h": buildable_length * 0.2}
    ]
    designs.append({"title": "Vastu Friendly (Kishan AI)", "rooms": d2_rooms})

    # Option 3: Compact Core (Central Corridor)
    d3_rooms = [
        {"name": "Corridor", "x": 3 + (buildable_width/2) - 1, "y": 3, "w": 2, "h": buildable_length},
        {"name": "Living", "x": 3, "y": 3, "w": (buildable_width/2) - 1, "h": buildable_length * 0.6},
        {"name": "Kitchen", "x": 3, "y": 3 + buildable_length * 0.6, "w": (buildable_width/2) - 1, "h": buildable_length * 0.4},
        {"name": "Bed 1", "x": 3 + (buildable_width/2) + 1, "y": 3, "w": (buildable_width/2) - 1, "h": buildable_length * 0.5},
        {"name": "Bed 2", "x": 3 + (buildable_width/2) + 1, "y": 3 + buildable_length * 0.5, "w": (buildable_width/2) - 1, "h": buildable_length * 0.5}
    ]
    designs.append({"title": "Compact Corridor (Kishan AI)", "rooms": d3_rooms})

    # Option 4: Open Plan (Living + Dining combined)
    d4_rooms = [
        {"name": "Living+Dining", "x": 3, "y": 3, "w": buildable_width, "h": buildable_length * 0.6},
        {"name": "Kitchen", "x": 3, "y": 3 + buildable_length * 0.6, "w": buildable_width * 0.4, "h": buildable_length * 0.4},
        {"name": "Bed", "x": 3 + buildable_width * 0.4, "y": 3 + buildable_length * 0.6, "w": buildable_width * 0.6, "h": buildable_length * 0.4}
    ]
    designs.append({"title": "Open Plan (Kishan AI)", "rooms": d4_rooms})

    # Option 5: L-Shape House
    d5_rooms = [
        {"name": "Living", "x": 3, "y": 3, "w": buildable_width * 0.6, "h": buildable_length},
        {"name": "Kitchen", "x": 3 + buildable_width * 0.6, "y": 3, "w": buildable_width * 0.4, "h": buildable_length * 0.5},
        {"name": "Bed", "x": 3 + buildable_width * 0.6, "y": 3 + buildable_length * 0.5, "w": buildable_width * 0.4, "h": buildable_length * 0.5}
    ]
    designs.append({"title": "L-Shape Design (Kishan AI)", "rooms": d5_rooms})

    # ३. BOQ (सिमेन्ट, स्टिल) र लागत हिसाब गर्ने
    for design in designs:
        builtup = sum([r["w"] * r["h"] for r in design["rooms"]])
        # नेपालको सामान्य दर अनुसार (प्रति वर्गफिट करिब ३५००)
        design["boq"] = {
            "cement_bags": int(builtup * 0.4),
            "steel_kg": int(builtup * 4),
            "bricks": int(builtup * 8)
        }
        design["est_cost_npr"] = builtup * 3500
    
    return designs

@app.route('/', methods=['GET', 'POST'])
def index():
    designs_data = None
    if request.method == 'POST':
        site_length = float(request.form.get('site_length', 30))
        site_width = float(request.form.get('site_width', 40))
        client_name = request.form.get('client_name', 'Client')
        location = request.form.get('location', 'Kathmandu')
        requirements = request.form.get('requirements', '2 Bedrooms')
        
        # 🧠 यहाँ हामीले हाम्रो आफ्नै "Kishan AI" इन्जिन चलाएका छौं
        ai_designs = generate_kishan_ai_designs(site_length, site_width, requirements)
        designs_data = []

        for i, design in enumerate(ai_designs):
            rooms = design.get("rooms", [])
            title = design.get("title", f"Option {i+1}")
            boq = design.get("boq", {})
            est_cost = design.get("est_cost_npr", 0)
            
            # AutoCAD DXF
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

            # PDF Report
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
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, height - 230, "2. ESTIMATED MATERIALS & COST")
            c.setFont("Helvetica", 11)
            c.drawString(40, height - 250, f"Cement: {boq.get('cement_bags', 0)} Bags")
            c.drawString(40, height - 265, f"Steel: {boq.get('steel_kg', 0)} Kg")
            c.drawString(40, height - 280, f"Bricks: {boq.get('bricks', 0)} Pcs")
            c.drawString(40, height - 295, f"Estimated Cost: NPR {est_cost:,.2f}")
            c.save()

            # 3D Render (Base64)
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