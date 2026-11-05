import ezdxf
from ezdxf import colors
import os

def create_dxf_from_ai():
    # १. यो तपाईंको AI ले दिएको डिजाइन हो (Vastu-Compliant Option)
    rooms = [
        {"name": "Living Room", "x": 0, "y": 0, "w": 6, "h": 8},
        {"name": "Staircase", "x": 6, "y": 0, "w": 6, "h": 8},
        {"name": "Family Lounge", "x": 0, "y": 8, "w": 6, "h": 8},
        {"name": "Puja Room", "x": 6, "y": 8, "w": 3, "h": 8},
        {"name": "Bathroom", "x": 9, "y": 8, "w": 3, "h": 8},
        {"name": "Bedroom 1", "x": 0, "y": 16, "w": 6, "h": 7},
        {"name": "Bedroom 2", "x": 6, "y": 16, "w": 6, "h": 7},
        {"name": "Kitchen", "x": 0, "y": 23, "w": 6, "h": 7},
        {"name": "Dining Area", "x": 6, "y": 23, "w": 6, "h": 7}
    ]

    # २. नयाँ AutoCAD फाइल बनाउने
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # लेयरहरू (AutoCAD को रङको लागि)
    doc.layers.add('WALLS', color=colors.WHITE)
    doc.layers.add('DOORS', color=colors.MAGENTA)
    doc.layers.add('WINDOWS', color=colors.CYAN)
    doc.layers.add('TEXT', color=colors.YELLOW)
    doc.layers.add('DIMENSIONS', color=colors.RED)

    # ३. कोठाहरू कोर्ने (पर्खाल र नाम)
    for r in rooms:
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        
        # पर्खाल (Wall Thickness 0.2m)
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 35})
        
        # कोठाको नाम
        text = msp.add_text(r["name"], dxfattribs={'layer': 'TEXT', 'height': 0.4})
        text.dxf.insert = (x + w/2, y + h/2)

        # ४. ढोका कोर्ने (प्रत्येक कोठाको तल्लो भित्तामा)
        door_x = x + (w/2) - 0.45
        msp.add_line((door_x, y), (door_x + 0.9, y), dxfattribs={'layer': 'DOORS', 'color': colors.RED})
        msp.add_arc((door_x, y), radius=0.9, start_angle=0, end_angle=90, dxfattribs={'layer': 'DOORS'})

        # ५. झ्याल कोर्ने (माथिल्लो भित्तामा)
        win_x = x + (w/2) - 0.75
        msp.add_line((win_x, y+h), (win_x + 1.5, y+h), dxfattribs={'layer': 'WINDOWS', 'lineweight': 30})
        msp.add_line((win_x, y+h+0.1), (win_x + 1.5, y+h+0.1), dxfattribs={'layer': 'WINDOWS', 'lineweight': 30})

    # ६. बाहिरी नाप (Dimensions)
    msp.add_linear_dim(base=(0, -2), p1=(0, 0), p2=(12, 0), dxfattribs={'layer': 'DIMENSIONS'}).render()
    msp.add_linear_dim(base=(-2, 0), p1=(0, 0), p2=(0, 30), angle=90, dxfattribs={'layer': 'DIMENSIONS'}).render()

    # ७. फाइल सेभ गर्ने
    out_dir = r"C:\Users\Msi\AIBrain\designs"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
        
    filepath = os.path.join(out_dir, "AI_Vastu_Design.dxf")
    doc.saveas(filepath)
    print(f"✅ AutoCAD DXF फाइल तयार भयो: {filepath}")
    os.startfile(out_dir)

if __name__ == "__main__":
    create_dxf_from_ai()
