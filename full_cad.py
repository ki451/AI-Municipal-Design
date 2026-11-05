import ezdxf
from ezdxf import colors
import os
import math

def create_full_working_drawing():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # लेयरहरू (AutoCAD को रङ)
    doc.layers.add('WALLS', color=colors.WHITE)
    doc.layers.add('DOORS', color=colors.MAGENTA)
    doc.layers.add('WINDOWS', color=colors.CYAN)
    doc.layers.add('TEXT', color=colors.YELLOW)
    doc.layers.add('DIMENSIONS', color=colors.RED)
    doc.layers.add('STRUCTURAL', color=colors.GREEN)

    # बक्स कोर्ने सहायक फंक्शन (किनभने add_rectangle हुँदैन)
    def draw_box(x1, y1, x2, y2, layer, lw=25):
        msp.add_lwpolyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], close=True, dxfattribs={'layer': layer, 'lineweight': lw})

    # ==========================================
    # १. GROUND FLOOR PLAN (X=0, Y=0)
    # ==========================================
    def draw_floor_plan(ox, oy):
        # बाहिरी पर्खाल
        draw_box(ox, oy, ox+12, oy+30, 'WALLS', 50)
        # भित्री पर्खालहरू
        msp.add_line((ox+6, oy), (ox+6, oy+30), dxfattribs={'layer': 'WALLS'})
        for y in [8, 16, 23]:
            msp.add_line((ox, oy+y), (ox+12, oy+y), dxfattribs={'layer': 'WALLS'})
        
        # कोठाको नाम
        msp.add_text("GROUND FLOOR PLAN", dxfattribs={'layer': 'TEXT', 'height': 0.8}).set_placement((ox+6, oy-3), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        
        # ढोका (Door Arc)
        msp.add_arc((ox+3, oy+8), radius=0.9, start_angle=180, end_angle=270, dxfattribs={'layer': 'DOORS'})
        msp.add_line((ox+3, oy+8), (ox+2.1, oy+8), dxfattribs={'layer': 'DOORS'})

        # झ्याल (Window)
        msp.add_line((ox+2, oy), (ox+4, oy), dxfattribs={'layer': 'WINDOWS', 'lineweight': 40})
        
        # नाप (Dimensions)
        msp.add_linear_dim(base=(ox, oy-2), p1=(ox, oy), p2=(ox+12, oy), dxfattribs={'layer': 'DIMENSIONS'}).render()
        msp.add_linear_dim(base=(ox-2, oy), p1=(ox, oy), p2=(ox, oy+30), angle=90, dxfattribs={'layer': 'DIMENSIONS'}).render()

    # ==========================================
    # २. FRONT ELEVATION (X=20, Y=0)
    # ==========================================
    def draw_elevation(ox, oy):
        msp.add_text("FRONT ELEVATION", dxfattribs={'layer': 'TEXT', 'height': 0.8}).set_placement((ox+6, oy-3), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        
        # जमिनको लाइन (Ground Line)
        msp.add_line((ox-2, oy), (ox+14, oy), dxfattribs={'layer': 'WALLS', 'lineweight': 50})
        
        # घरको मुख्य भाग (3 तल्ला)
        draw_box(ox, oy, ox+12, oy+3.2, 'WALLS')
        draw_box(ox, oy+3.5, ox+12, oy+6.7, 'WALLS')
        draw_box(ox, oy+7.0, ox+12, oy+10.2, 'WALLS')
        
        # छाना (Parapet/Roof)
        msp.add_line((ox-0.2, oy+10.2), (ox+12.2, oy+10.2), dxfattribs={'layer': 'WALLS', 'lineweight': 50})
        
        # झ्यालहरू (Windows on Elevation)
        for y in [1, 4.5, 8]:
            draw_box(ox+1, oy+y, ox+3, oy+y+1.5, 'WINDOWS', 30)
            draw_box(ox+9, oy+y, ox+11, oy+y+1.5, 'WINDOWS', 30)
        
        # मुख्य ढोका (Main Door)
        draw_box(ox+5, oy, ox+7, oy+2.1, 'DOORS', 30)

    # ==========================================
    # ३. SECTION A-A (X=0, Y=40)
    # ==========================================
    def draw_section(ox, oy):
        msp.add_text("SECTION A-A", dxfattribs={'layer': 'TEXT', 'height': 0.8}).set_placement((ox+6, oy-3), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        
        # जमिनको लाइन
        msp.add_line((ox-2, oy), (ox+14, oy), dxfattribs={'layer': 'WALLS', 'lineweight': 50})
        
        # जग (Foundation)
        draw_box(ox+1, oy-1, ox+3, oy, 'STRUCTURAL')
        draw_box(ox+9, oy-1, ox+11, oy, 'STRUCTURAL')
        
        # तल्लाहरू (Slabs) र उचाइ
        for h in [3.2, 6.7, 10.2]:
            msp.add_line((ox, oy+h), (ox+12, oy+h), dxfattribs={'layer': 'WALLS', 'lineweight': 40})
            
        # सिँढी (Staircase representation)
        for i in range(10):
            msp.add_line((ox+4+i*0.2, oy), (ox+4+i*0.2, oy+3.2), dxfattribs={'layer': 'STRUCTURAL'})

    # ==========================================
    # ४. STRUCTURAL LAYOUT (X=20, Y=40)
    # ==========================================
    def draw_structural(ox, oy):
        msp.add_text("STRUCTURAL LAYOUT", dxfattribs={'layer': 'TEXT', 'height': 0.8}).set_placement((ox+6, oy-3), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        
        # ग्रिड लाइनहरू (Grid Lines)
        for x in [0, 6, 12]:
            msp.add_line((ox+x, oy), (ox+x, oy+30), dxfattribs={'layer': 'DIMENSIONS'})
        for y in [0, 8, 16, 23, 30]:
            msp.add_line((ox, oy+y), (ox+12, oy+y), dxfattribs={'layer': 'DIMENSIONS'})
            
        # पिलरहरू (Columns - 9x9 inch)
        for x in [0, 6, 12]:
            for y in [0, 8, 16, 23, 30]:
                draw_box(ox+x-0.2, oy+y-0.2, ox+x+0.2, oy+y+0.2, 'STRUCTURAL', 50)

    # ==========================================
    # ५. सबै पानाहरू कोर्ने (Grid Layout)
    # ==========================================
    draw_floor_plan(0, 0)
    draw_elevation(20, 0)
    draw_section(0, 40)
    draw_structural(20, 40)

    # सेभ गर्ने
    out_dir = r"C:\Users\Msi\AIBrain\designs"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    filepath = os.path.join(out_dir, "Full_Working_Drawing.dxf")
    doc.saveas(filepath)
    print(f"✅ सबै ४ पाना (Floor Plan, Elevation, Section, Structural) सहितको CAD फाइल तयार भयो: {filepath}")
    os.startfile(out_dir)

if __name__ == "__main__":
    create_full_working_drawing()
