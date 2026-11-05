import ezdxf
from ezdxf import colors
import os

def create_clean_dxf():
    # १. AI ले दिएको डिजाइन (Vastu-Compliant) को सही कोअर्डिनेट
    # यहाँ हामीले सबै पर्खालहरू ठ्याक्कै जोडिएको (0, 6, 12) र (0, 8, 16, 23, 30) मा मिलाएका छौं।
    rooms = [
        # Left Side
        {"name": "LIVING", "x": 0, "y": 0, "w": 6, "h": 8},
        {"name": "FAMILY", "x": 0, "y": 8, "w": 6, "h": 8},
        {"name": "BEDROOM 1", "x": 0, "y": 16, "w": 6, "h": 7},
        {"name": "KITCHEN", "x": 0, "y": 23, "w": 6, "h": 7},
        
        # Right Side
        {"name": "STAIR", "x": 6, "y": 0, "w": 6, "h": 8},
        {"name": "PUJA", "x": 6, "y": 8, "w": 3, "h": 8},
        {"name": "BATH", "x": 9, "y": 8, "w": 3, "h": 8},
        {"name": "BEDROOM 2", "x": 6, "y": 16, "w": 6, "h": 7},
        {"name": "DINING", "x": 6, "y": 23, "w": 6, "h": 7}
    ]

    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # लेयरहरू
    doc.layers.add('WALLS', color=colors.WHITE)
    doc.layers.add('DOORS', color=colors.MAGENTA)
    doc.layers.add('WINDOWS', color=colors.CYAN)
    doc.layers.add('TEXT', color=colors.YELLOW)
    doc.layers.add('DIMENSIONS', color=colors.RED)

    # २. पर्खाल कोर्ने (Double Line Wall - मोटाई 0.2m)
    # बाहिरी पर्खाल
    msp.add_lwpolyline([(0,0), (12,0), (12,30), (0,30)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 50})
    msp.add_lwpolyline([(0.2,0.2), (11.8,0.2), (11.8,29.8), (0.2,29.8)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 50})
    
    # भित्री पर्खालहरू (Vertical)
    msp.add_line((6, 0), (6, 30), dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    msp.add_line((6.2, 0), (6.2, 30), dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    
    # भित्री पर्खालहरू (Horizontal - Left)
    msp.add_line((0, 8), (6, 8), dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    msp.add_line((0, 16), (6, 16), dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    msp.add_line((0, 23), (6, 23), dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    
    # भित्री पर्खालहरू (Horizontal - Right)
    msp.add_line((6, 8), (12, 8), dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    msp.add_line((6, 16), (12, 16), dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    msp.add_line((6, 23), (12, 23), dxfattribs={'layer': 'WALLS', 'lineweight': 35})

    # Puja र Bath बीचको पर्खाल
    msp.add_line((9, 8), (9, 16), dxfattribs={'layer': 'WALLS', 'lineweight': 35})

    # ३. कोठाको नाम राख्ने
    for r in rooms:
        cx = r["x"] + r["w"]/2
        cy = r["y"] + r["h"]/2
        text = msp.add_text(r["name"], dxfattribs={'layer': 'TEXT', 'height': 0.6})
        text.dxf.insert = (cx, cy)

    # ४. ढोका कोर्ने (Door arcs)
    msp.add_arc((4, 8), radius=1.0, start_angle=180, end_angle=270, dxfattribs={'layer': 'DOORS'})
    msp.add_arc((6, 12), radius=1.0, start_angle=0, end_angle=90, dxfattribs={'layer': 'DOORS'})
    
    # ५. झ्याल कोर्ने (Windows)
    msp.add_line((2, 0), (4, 0), dxfattribs={'layer': 'WINDOWS', 'lineweight': 40})
    msp.add_line((2, 0.1), (4, 0.1), dxfattribs={'layer': 'WINDOWS', 'lineweight': 40})
    msp.add_line((8, 30), (10, 30), dxfattribs={'layer': 'WINDOWS', 'lineweight': 40})
    msp.add_line((8, 29.9), (10, 29.9), dxfattribs={'layer': 'WINDOWS', 'lineweight': 40})

    # ६. नाप (Dimensions)
    msp.add_linear_dim(base=(0, -2), p1=(0, 0), p2=(12, 0), dxfattribs={'layer': 'DIMENSIONS'}).render()
    msp.add_linear_dim(base=(-2, 0), p1=(0, 0), p2=(0, 30), angle=90, dxfattribs={'layer': 'DIMENSIONS'}).render()

    out_dir = r"C:\Users\Msi\AIBrain\designs"
    filepath = os.path.join(out_dir, "Clean_Municipality_Plan.dxf")
    doc.saveas(filepath)
    print(f"✅ सफा CAD फाइल तयार भयो: {filepath}")
    os.startfile(out_dir)

if __name__ == "__main__":
    create_clean_dxf()
