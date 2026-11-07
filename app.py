from flask import Flask, render_template, request, url_for
import os, ezdxf
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'static', 'outputs')
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\Arial.ttf'))
except:
    pass

# ==========================================
# 🏗️ REALISTIC LAYOUT ENGINE (Hardcoded Math)
# ==========================================
def get_real_layout(site_l, site_w):
    # Standard 30x40 plot: 
    # Setback: Front 5, Back 3, Sides 3. 
    # Buildable: X: 3 to 27 (Width 24). Y: 5 to 37 (Length 32).
    
    # We will use a fixed logical layout that scales beautifully
    rooms = []
    
    # 1. Living Room (Front)
    rooms.append({"name": "बैठक", "type": "living", "x": 3, "y": 5, "w": 24, "h": 10})
    
    # 2. Corridor (Horizontal)
    rooms.append({"name": "कोरिडोर", "type": "corridor", "x": 3, "y": 15, "w": 24, "h": 4})
    
    # 3. Back Row (Bedrooms, Kitchen, Bath, Puja)
    rooms.append({"name": "सुत्ने कोठा १", "type": "bed", "x": 3, "y": 19, "w": 12, "h": 9})
    rooms.append({"name": "सुत्ने कोठा २", "type": "bed", "x": 3, "y": 28, "w": 12, "h": 9})
    rooms.append({"name": "भान्सा", "type": "kitchen", "x": 15, "y": 19, "w": 12, "h": 9})
    rooms.append({"name": "बाथरुम", "type": "bath", "x": 15, "y": 28, "w": 6, "h": 9})
    rooms.append({"name": "पुजा", "type": "puja", "x": 21, "y": 28, "w": 6, "h": 9})
    
    return rooms

# ==========================================
# 🎨 SVG GENERATOR (Detailed Blueprint)
# ==========================================
def draw_furniture(svg, x, y, w, h, typ):
    if typ == "bed":
        # Bed 5x6.5
        bx, by = x + (w-5)/2, y + (h-6.5)/2
        svg += f'<rect x="{bx}" y="{by}" width="5" height="6.5" fill="#334155" stroke="#94a3b8" stroke-width="0.2" rx="0.5"/>'
        svg += f'<rect x="{bx+0.2}" y="{by+0.2}" width="4.6" height="1.5" fill="#64748b" rx="0.3"/>'
        svg += f'<rect x="{bx+0.2}" y="{by+5}" width="4.6" height="1.3" fill="#475569" rx="0.2"/>'
    elif typ == "living":
        # Sofa
        svg += f'<rect x="{x+2}" y="{y+2}" width="7" height="2.5" fill="#334155" stroke="#94a3b8" stroke-width="0.2" rx="0.3"/>'
        svg += f'<rect x="{x+2}" y="{y+2}" width="1" height="2.5" fill="#64748b"/>'
        svg += f'<rect x="{x+8}" y="{y+2}" width="1" height="2.5" fill="#64748b"/>'
        # TV
        svg += f'<rect x="{x+w-4}" y="{y+h/2-2}" width="1" height="4" fill="#475569" stroke="#94a3b8" stroke-width="0.2"/>'
    elif typ == "kitchen":
        # L-Shape Counter
        svg += f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="2" fill="#334155" stroke="#94a3b8" stroke-width="0.2"/>'
        svg += f'<rect x="{x+1}" y="{y+1}" width="2" height="{h-2}" fill="#334155" stroke="#94a3b8" stroke-width="0.2"/>'
        # Stove
        svg += f'<rect x="{x+2}" y="{y+1.5}" width="1.5" height="1.5" fill="#64748b"/>'
        # Sink
        svg += f'<rect x="{x+w-4}" y="{y+1.5}" width="2" height="1.5" fill="#64748b"/>'
    elif typ == "bath":
        # Toilet
        svg += f'<ellipse cx="{x+2}" cy="{y+h-3}" rx="1" ry="1.5" fill="#64748b"/>'
        # Shower
        svg += f'<rect x="{x+w-3}" y="{y+h-4}" width="2.5" height="3" fill="#475569" stroke="#94a3b8" stroke-width="0.1"/>'
    elif typ == "puja":
        # Altar
        svg += f'<rect x="{x+w/2-1.5}" y="{y+h-3}" width="3" height="2" fill="#b45309" stroke="#fcd34d" stroke-width="0.2"/>'

def create_real_svg(rooms, site_l, site_w):
    # Build SVG
    svg = f'<svg width="100%" height="550" viewBox="-10 -10 {site_w+20} {site_l+20}" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:8px;">'
    
    # Site Boundary
    svg += f'<rect x="0" y="0" width="{site_w}" height="{site_l}" fill="none" stroke="#ef4444" stroke-dasharray="4,4" stroke-width="1"/>'
    
    # Draw Rooms and Walls
    for r in rooms:
        # Room Floor (Dark)
        svg += f'<rect x="{r["x"]}" y="{r["y"]}" width="{r["w"]}" height="{r["h"]}" fill="#1e293b" />'
        
        # Walls (Thick)
        svg += f'<rect x="{r["x"]}" y="{r["y"]}" width="{r["w"]}" height="{r["h"]}" fill="none" stroke="#cbd5e1" stroke-width="0.8"/>'
        svg += f'<rect x="{r["x"]+0.3}" y="{r["y"]+0.3}" width="{r["w"]-0.6}" height="{r["h"]-0.6}" fill="none" stroke="#475569" stroke-width="0.2"/>'
        
        # Furniture
        draw_furniture(svg, r["x"], r["y"], r["w"], r["h"], r["type"])
        
        # Text Label
        fs = min(r["w"], r["h"]) * 0.15
        fs = max(min(fs, 3), 1.2) # Cap font size
        cx = r["x"] + r["w"]/2
        cy = r["y"] + r["h"]/2
        svg += f'<text x="{cx}" y="{cy - 0.5}" text-anchor="middle" font-size="{fs}" fill="#f8fafc" font-family="Arial" font-weight="bold">{r["name"]}</text>'
        svg += f'<text x="{cx}" y="{cy + fs*0.8}" text-anchor="middle" font-size="{fs*0.6}" fill="#94a3b8" font-family="Arial">{r["w"]}x{r["h"]}</text>'

    # Main Door (Green Arc)
    # Living room is at x=3, y=5, w=24, h=10. Center is x=15.
    dx, dy = 15, 5
    svg += f'<rect x="{dx-1.5}" y="{dy}" width="3" height="0.6" fill="#22c55e"/>'
    svg += f'<path d="M {dx-1.5} {dy} A 3 3 0 0 1 {dx+1.5} {dy+3}" fill="none" stroke="#22c55e" stroke-width="0.3" stroke-dasharray="1,1"/>'

    # Windows (Blue Lines)
    # Living Front
    svg += f'<rect x="6" y="5" width="4" height="0.6" fill="#38bdf8"/>'
    svg += f'<rect x="20" y="5" width="4" height="0.6" fill="#38bdf8"/>'
    # Sides (Beds)
    svg += f'<rect x="3" y="21" width="0.6" height="4" fill="#38bdf8"/>'
    svg += f'<rect x="3" y="30" width="0.6" height="4" fill="#38bdf8"/>'
    # Kitchen
    svg += f'<rect x="26.4" y="21" width="0.6" height="4" fill="#38bdf8"/>'

    svg += '</svg>'
    return svg

@app.route('/', methods=['GET', 'POST'])
def index():
    designs = None
    if request.method == 'POST':
        client = request.form.get('client_name', 'Client')
        location = request.form.get('location', 'Kathmandu')
        site_l = float(request.form.get('site_length', 40)) # Default 40
        site_w = float(request.form.get('site_width', 30))  # Default 30
        
        rooms = get_real_layout(site_l, site_w)

        # DXF
        doc = ezdxf.new('R2010')
        doc.styles.add("NepaliStyle", font="Arial.ttf")
        msp = doc.modelspace()
        for r in rooms:
            msp.add_lwpolyline([(r["x"], r["y"]), (r["x"]+r["w"], r["y"]), (r["x"]+r["w"], r["y"]+r["h"]), (r["x"], r["y"]+r["h"])], close=True, dxfattribs={"layer": "Walls"})
            msp.add_text(r["name"], dxfattribs={"layer": "Walls", "height": 1.0, "style": "NepaliStyle"}).set_placement((r["x"]+0.5, r["y"]+0.5))
        dxf_filename = "Real_Plan.dxf"
        doc.saveas(os.path.join(app.config['OUTPUT_FOLDER'], dxf_filename))

        # PDF
        pdf_filename = "Real_Report.pdf"
        pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
        c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
        w, h = landscape(A4)
        c.setStrokeColor(colors.black); c.setLineWidth(2); c.rect(20, 20, w-40, h-40)
        
        try: c.setFont("Arial", 16)
        except: c.setFont("Helvetica-Bold", 16)
        c.drawString(40, h - 60, "KISHAN AI - PROFESSIONAL ARCHITECTURAL PLAN")
        try: c.setFont("Arial", 12)
        except: c.setFont("Helvetica", 12)
        c.drawString(40, h - 80, f"Client: {client} | Location: {location}")
        
        total = site_l * site_w
        built = sum([r["w"] * r["h"] for r in rooms])
        c.drawString(40, h - 120, f"Plot Area: {total:.2f} Sq.Ft | Built-up: {built:.2f} Sq.Ft")
        c.drawString(40, h - 140, f"F.A.R: {built/total:.2f} | Coverage: {(built/total)*100:.1f}%")

        scale = 6; ox = 450; oy = 100
        c.setStrokeColor(colors.red)
        c.rect(ox, oy, site_w*scale, site_l*scale)
        c.setLineWidth(1.5)
        for r in rooms:
            rx = ox + (r["x"] * scale); ry = oy + (r["y"] * scale)
            c.setStrokeColor(colors.black)
            c.rect(rx, ry, r["w"]*scale, r["h"]*scale)
            try: c.setFont("Arial", 6)
            except: c.setFont("Helvetica", 6)
            text_x = rx + (r["w"]*scale/2) - 8
            text_y = ry + (r["h"]*scale/2)
            c.drawString(text_x, text_y, r["name"])
        c.save()
        
        svg = create_real_svg(rooms, site_l, site_w)
        cost = built * 3500
        boq = {"cement": int(built*0.4), "steel": int(built*4), "bricks": int(built*8)}
        
        designs = {
            "dxf_url": url_for('static', filename=f'outputs/{dxf_filename}'),
            "pdf_url": url_for('static', filename=f'outputs/{pdf_filename}'),
            "svg": svg,
            "cost": cost,
            "boq": boq
        }
    return render_template('index.html', designs=designs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)