import ezdxf
from ezdxf import colors
import os
import math

def create_master_floor_plan():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # १. लेयरहरू (AutoCAD मा रङ र मोटाई छुट्याउन)
    doc.layers.add('WALLS', color=colors.WHITE)
    doc.layers.add('DOORS', color=colors.MAGENTA)
    doc.layers.add('WINDOWS', color=colors.CYAN)
    doc.layers.add('TEXT', color=colors.YELLOW)
    doc.layers.add('DIMENSIONS', color=colors.RED)
    doc.layers.add('TITLE_BLOCK', color=colors.GRAY)

    # २. पर्खालहरू (Wall Thickness: बाहिरी 0.23m, भित्री 0.11m)
    # यो लेआउट १२x३० को घरको लागि हो (ठ्याक्कै मिलाएर)
    wall_ext = 0.23
    wall_int = 0.11

    # बाहिरी पर्खाल (Outer Walls)
    msp.add_lwpolyline([(0,0), (12,0), (12,30), (0,30)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 50})
    
    # भित्री पर्खालहरू (Inner Walls - Vertical)
    msp.add_lwpolyline([(6,0), (6.11,0), (6.11,30), (6,30)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 35})
    
    # भित्री पर्खालहरू (Horizontal - Left)
    for y in [8, 16, 23]:
        msp.add_lwpolyline([(0,y), (6,y), (6,y+0.11), (0,y+0.11)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 35})
        
    # भित्री पर्खालहरू (Horizontal - Right)
    for y in [8, 16, 23]:
        msp.add_lwpolyline([(6,y), (12,y), (12,y+0.11), (6,y+0.11)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 35})

    # ३. कोठाको नाम र साइज (Text)
    def add_room(name, x, y, w, h):
        cx, cy = x + w/2, y + h/2
        # कोठाको नाम
        msp.add_text(name, dxfattribs={'layer': 'TEXT', 'height': 0.35}).set_placement((cx, cy+0.3), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        # कोठाको नाप
        msp.add_text(f"{w}m x {h}m", dxfattribs={'layer': 'TEXT', 'height': 0.25}).set_placement((cx, cy-0.4), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    add_room("LIVING", 0, 0, 6, 8)
    add_room("FAMILY", 0, 8, 6, 8)
    add_room("BED 1", 0, 16, 6, 7)
    add_room("KITCHEN", 0, 23, 6, 7)
    
    add_room("STAIR", 6.11, 0, 5.89, 8)
    add_room("PUJA", 6.11, 8, 2.8, 8)
    add_room("BATH", 9.1, 8, 2.9, 8)
    add_room("BED 2", 6.11, 16, 5.89, 7)
    add_room("DINING", 6.11, 23, 5.89, 7)

    # ४. ढोका (Doors - Standard 0.9m Width)
    def draw_door(x, y, angle, flip=False):
        w = 0.9
        rad = math.radians(angle)
        if not flip:
            end_x, end_y = x + math.cos(rad)*w, y + math.sin(rad)*w
            msp.add_arc((x, y), radius=w, start_angle=angle, end_angle=angle+90, dxfattribs={'layer': 'DOORS'})
        else:
            end_x, end_y = x - math.cos(rad)*w, y - math.sin(rad)*w
            msp.add_arc((x, y), radius=w, start_angle=angle-90, end_angle=angle, dxfattribs={'layer': 'DOORS'})
        msp.add_line((x, y), (end_x, end_y), dxfattribs={'layer': 'DOORS'})

    draw_door(3, 8, 180)     # Living to Family
    draw_door(6, 4, 270)     # Stair to Living
    draw_door(6, 12, 0)      # Family to Puja
    draw_door(9, 8.5, 270)   # Puja to Bath
    draw_door(3, 16, 180)    # Family to Bed 1
    draw_door(6, 20, 0)      # Stair to Bed 2
    draw_door(3, 23, 180)    # Bed 1 to Kitchen

    # ५. झ्याल (Windows - 1.5m Width)
    def draw_window(x1, y1, x2, y2):
        msp.add_line((x1, y1), (x2, y2), dxfattribs={'layer': 'WINDOWS', 'lineweight': 40})
        msp.add_line((x1, y1+0.1), (x2, y2+0.1), dxfattribs={'layer': 'WINDOWS', 'lineweight': 40})

    draw_window(1.5, 0, 4.5, 0)     # Living Front
    draw_window(8, 0, 10, 0)        # Stair Front
    draw_window(1.5, 30, 4.5, 30)   # Kitchen Back
    draw_window(8, 30, 10, 30)      # Dining Back
    draw_window(0, 4, 0, 6)         # Living Side

    # ६. नाप (Dimensions)
    msp.add_linear_dim(base=(0, -2), p1=(0, 0), p2=(12, 0), dxfattribs={'layer': 'DIMENSIONS'}).render()
    msp.add_linear_dim(base=(-2, 0), p1=(0, 0), p2=(0, 30), angle=90, dxfattribs={'layer': 'DIMENSIONS'}).render()

    # ७. प्रोफेसनल Title Block (तलको बक्स)
    tb_x, tb_y = 0, -12
    msp.add_lwpolyline([(tb_x, tb_y), (tb_x+12, tb_y), (tb_x+12, tb_y-4), (tb_x, tb_y-4)], close=True, dxfattribs={'layer': 'TITLE_BLOCK', 'lineweight': 50})
    msp.add_line((tb_x, tb_y-2), (tb_x+12, tb_y-2), dxfattribs={'layer': 'TITLE_BLOCK'})
    msp.add_line((tb_x+6, tb_y-2), (tb_x+6, tb_y-4), dxfattribs={'layer': 'TITLE_BLOCK'})
    
    msp.add_text("PROPOSED RESIDENTIAL BUILDING", dxfattribs={'layer': 'TITLE_BLOCK', 'height': 0.4}).set_placement((tb_x+6, tb_y-1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text("GROUND FLOOR PLAN", dxfattribs={'layer': 'TITLE_BLOCK', 'height': 0.3}).set_placement((tb_x+3, tb_y-3), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text("SCALE: 1:100", dxfattribs={'layer': 'TITLE_BLOCK', 'height': 0.2}).set_placement((tb_x+9, tb_y-3), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # ८. सेभ गर्ने
    out_dir = r"C:\Users\Msi\AIBrain\designs"
    filepath = os.path.join(out_dir, "Page1_Professional_Plan.dxf")
    doc.saveas(filepath)
    print(f"✅ AutoCAD स्ट्यान्डर्डको फ्लोर प्लान तयार भयो: {filepath}")
    os.startfile(out_dir)

if __name__ == "__main__":
    create_master_floor_plan()
