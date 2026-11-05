import ezdxf
from ezdxf import colors
import math
import os

def draw_room(msp, x, y, w, l, label):
    # वास्तविक पर्खाल (मोटो लाइन)
    msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+l), (x, y+l)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    # कोठाको नाम
    msp.add_text(label, dxfattribs={'layer': 'TEXT', 'height': 0.4}).set_placement((x+w/2, y+l/2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    
def draw_door(msp, x, y, angle, width=0.9):
    # ढोका (Arc र Line)
    msp.add_line((x, y), (x + math.cos(math.radians(angle))*width, y + math.sin(math.radians(angle))*width), dxfattribs={'layer': 'DOORS'})
    msp.add_arc((x, y), radius=width, start_angle=angle, end_angle=angle+90, dxfattribs={'layer': 'DOORS'})

def draw_window(msp, x1, y1, x2, y2):
    # झ्याल (Double Line)
    msp.add_line((x1, y1), (x2, y2), dxfattribs={'layer': 'WINDOWS', 'lineweight': 30})
    msp.add_line((x1, y1+0.1), (x2, y2+0.1), dxfattribs={'layer': 'WINDOWS', 'lineweight': 30})

def create_dxf(filename, layout_data):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # लेयरहरू (AutoCAD मा रङ छुट्याउन)
    doc.layers.add('WALLS', color=colors.WHITE)
    doc.layers.add('DOORS', color=colors.MAGENTA)
    doc.layers.add('WINDOWS', color=colors.CYAN)
    doc.layers.add('TEXT', color=colors.YELLOW)
    doc.layers.add('DIMENSIONS', color=colors.RED)
    
    # घरको बाहिरी सिमाना (12m x 30m)
    msp.add_lwpolyline([(0,0), (12,0), (12,30), (0,30)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 50})
    
    for room in layout_data:
        draw_room(msp, room['x'], room['y'], room['w'], room['l'], room['name'])
        if 'door' in room:
            draw_door(msp, room['door'][0], room['door'][1], room['door'][2])
        if 'window' in room:
            draw_window(msp, room['window'][0], room['window'][1], room['window'][2], room['window'][3])
            
    # नाप (Dimensions)
    msp.add_linear_dim(base=(0, -2), p1=(0, 0), p2=(12, 0), dxfattribs={'layer': 'DIMENSIONS'}).render()
    msp.add_linear_dim(base=(-2, 0), p1=(0, 0), p2=(0, 30), angle=90, dxfattribs={'layer': 'DIMENSIONS'}).render()
    
    doc.saveas(filename)
    print(f"✅ तयार भयो: {os.path.basename(filename)}")

def main():
    out_dir = r"C:\Users\Msi\AIBrain\designs"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
        
    layouts = {}
    
    # अप्सन १: स्ट्यान्डर्ड (Living अगाडि, Kitchen पछाडि)
    layouts["1_Standard_Plan.dxf"] = [
        {'name': 'LIVING', 'x': 0, 'y': 0, 'w': 6, 'l': 8, 'window': (1,0,4,0)},
        {'name': 'KITCHEN', 'x': 0, 'y': 8, 'w': 6, 'l': 4, 'door': (3, 8, 0)},
        {'name': 'STAIR', 'x': 0, 'y': 12, 'w': 3, 'l': 4},
        {'name': 'BATH', 'x': 3, 'y': 12, 'w': 3, 'l': 4, 'door': (3, 12, 0)},
        {'name': 'PARKING', 'x': 0, 'y': 16, 'w': 6, 'l': 6, 'window': (1,16,4,16)},
        {'name': 'PUJA', 'x': 0, 'y': 22, 'w': 4, 'l': 4, 'door': (2, 22, 90)},
        {'name': 'BEDROOM 1', 'x': 6, 'y': 0, 'w': 6, 'l': 6, 'window': (7,0,10,0)},
        {'name': 'BEDROOM 2', 'x': 6, 'y': 6, 'w': 6, 'l': 6, 'door': (6, 8, 180)},
        {'name': 'CORRIDOR', 'x': 6, 'y': 12, 'w': 2, 'l': 18},
        {'name': 'BEDROOM 3', 'x': 8, 'y': 12, 'w': 4, 'l': 9, 'door': (8, 15, 180)},
        {'name': 'BEDROOM 4', 'x': 8, 'y': 21, 'w': 4, 'l': 9, 'window': (9,30,11,30)}
    ]
    
    # अप्सन २: लामो करिडोर (बीचमा)
    layouts["2_Central_Corridor.dxf"] = [
        {'name': 'CORRIDOR', 'x': 5, 'y': 0, 'w': 2, 'l': 30},
        {'name': 'LIVING', 'x': 0, 'y': 0, 'w': 5, 'l': 10, 'window': (1,0,3,0)},
        {'name': 'DINING', 'x': 0, 'y': 10, 'w': 5, 'l': 6, 'door': (2, 10, 0)},
        {'name': 'KITCHEN', 'x': 0, 'y': 16, 'w': 5, 'l': 5, 'door': (2, 16, 0)},
        {'name': 'STAIR', 'x': 0, 'y': 21, 'w': 5, 'l': 9},
        {'name': 'BEDROOM 1', 'x': 7, 'y': 0, 'w': 5, 'l': 8, 'window': (8,0,11,0)},
        {'name': 'BATH', 'x': 7, 'y': 8, 'w': 5, 'l': 4, 'door': (7, 10, 180)},
        {'name': 'BEDROOM 2', 'x': 7, 'y': 12, 'w': 5, 'l': 8, 'window': (8,12,11,12)},
        {'name': 'BEDROOM 3', 'x': 7, 'y': 20, 'w': 5, 'l': 6, 'door': (7, 22, 180)},
        {'name': 'PUJA', 'x': 7, 'y': 26, 'w': 5, 'l': 4}
    ]
    
    # अप्सन ३: अगाडि ठूलो आँगन (Courtyard Focus)
    layouts["3_Courtyard_Focus.dxf"] = [
        {'name': 'CORRIDOR', 'x': 0, 'y': 10, 'w': 12, 'l': 2},
        {'name': 'LIVING', 'x': 0, 'y': 0, 'w': 8, 'l': 10, 'window': (1,0,6,0)},
        {'name': 'STAIR', 'x': 8, 'y': 0, 'w': 4, 'l': 5},
        {'name': 'BATH', 'x': 8, 'y': 5, 'w': 4, 'l': 5, 'door': (8, 8, 180)},
        {'name': 'KITCHEN', 'x': 0, 'y': 12, 'w': 5, 'l': 8, 'door': (2, 12, 0)},
        {'name': 'BEDROOM 1', 'x': 5, 'y': 12, 'w': 7, 'l': 8, 'window': (8,12,10,12)},
        {'name': 'BEDROOM 2', 'x': 0, 'y': 20, 'w': 6, 'l': 10, 'door': (3, 20, 0)},
        {'name': 'BEDROOM 3', 'x': 6, 'y': 20, 'w': 6, 'l': 6, 'window': (7,20,9,20)},
        {'name': 'PUJA', 'x': 6, 'y': 26, 'w': 6, 'l': 4}
    ]
    
    # अप्सन ४: खुला भान्सा र बैठक (Open Plan)
    layouts["4_Open_Plan.dxf"] = [
        {'name': 'LIVING + DINING', 'x': 0, 'y': 0, 'w': 7, 'l': 12, 'window': (1,0,6,0)},
        {'name': 'KITCHEN', 'x': 7, 'y': 0, 'w': 5, 'l': 6, 'door': (7, 3, 180)},
        {'name': 'STAIR + BATH', 'x': 7, 'y': 6, 'w': 5, 'l': 6},
        {'name': 'BEDROOM 1', 'x': 0, 'y': 12, 'w': 7, 'l': 6, 'door': (3, 12, 0)},
        {'name': 'BEDROOM 2', 'x': 7, 'y': 12, 'w': 5, 'l': 6, 'window': (8,12,11,12)},
        {'name': 'BEDROOM 3', 'x': 0, 'y': 18, 'w': 7, 'l': 6, 'window': (1,18,5,18)},
        {'name': 'BEDROOM 4', 'x': 7, 'y': 18, 'w': 5, 'l': 6},
        {'name': 'BALCONY', 'x': 0, 'y': 24, 'w': 12, 'l': 6, 'window': (2,30,10,30)},
    ]

    # अप्सन ५: कम्प्याक्ट कोर (सिँढी र बाथ बीचमा)
    layouts["5_Compact_Core.dxf"] = [
        {'name': 'LIVING', 'x': 0, 'y': 0, 'w': 12, 'l': 8, 'window': (2,0,9,0)},
        {'name': 'KITCHEN', 'x': 0, 'y': 8, 'w': 4, 'l': 5, 'door': (2, 8, 0)},
        {'name': 'CORRIDOR', 'x': 4, 'y': 8, 'w': 2, 'l': 22},
        {'name': 'BATH', 'x': 6, 'y': 8, 'w': 3, 'l': 5, 'door': (6, 10, 180)},
        {'name': 'STAIR', 'x': 9, 'y': 8, 'w': 3, 'l': 5},
        {'name': 'BEDROOM 1', 'x': 0, 'y': 13, 'w': 4, 'l': 6, 'door': (2, 13, 0)},
        {'name': 'BEDROOM 2', 'x': 6, 'y': 13, 'w': 6, 'l': 6, 'window': (7,13,10,13)},
        {'name': 'BEDROOM 3', 'x': 0, 'y': 19, 'w': 6, 'l': 7, 'window': (1,19,4,19)},
        {'name': 'PUJA', 'x': 6, 'y': 19, 'w': 6, 'l': 7, 'door': (9, 19, 180)},
        {'name': 'PARKING', 'x': 0, 'y': 26, 'w': 12, 'l': 4, 'window': (2,26,9,26)},
    ]

    print("🏗️ ५ वटा वास्तविक CAD डिजाइनहरू बन्दै...")
    for filename, data in layouts.items():
        filepath = os.path.join(out_dir, filename)
        create_dxf(filepath, data)
        
    print("\n🎉 सबै ५ वटा नगरपालिका-स्तरका डिजाइनहरू तयार भए!")
    os.startfile(out_dir)

if __name__ == "__main__":
    main()
