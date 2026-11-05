import ezdxf
from ezdxf import colors
import math

def create_municipality_blueprint():
    # १. नयाँ DXF फाइल र लेयरहरू बनाउने
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # लेयरहरू (AutoCAD को लागि)
    doc.layers.add('WALLS', color=colors.WHITE)
    doc.layers.add('DOORS', color=colors.MAGENTA)
    doc.layers.add('WINDOWS', color=colors.CYAN)
    doc.layers.add('TEXT', color=colors.YELLOW)
    doc.layers.add('DIMENSIONS', color=colors.RED)
    doc.layers.add('FURNITURE', color=colors.GREEN)

    # २. घरको मुख्य भित्ता (Outer Boundary - 12m x 30m)
    # पर्खाल 0.2m (8 इन्च) मोटो मानिएको छ
    wall_thickness = 0.2
    
    # बाहिरी पर्खाल
    msp.add_lwpolyline([(0,0), (12,0), (12,30), (0,30)], close=True, dxfattribs={'layer': 'WALLS', 'lineweight': 35})

    # ३. भित्री पर्खालहरू (Internal Walls)
    # करिडोरको लागि बीचमा २ मिटरको ठाउँ (x=4.9 देखि x=7.1 सम्म)
    msp.add_line((4.9, 0), (4.9, 30), dxfattribs={'layer': 'WALLS'})
    msp.add_line((7.1, 0), (7.1, 30), dxfattribs={'layer': 'WALLS'})
    
    # तल्ला अनुसार कोठा छुट्याउने पर्खाल (Horizontal)
    msp.add_line((0, 8), (4.9, 8), dxfattribs={'layer': 'WALLS'})   # बायाँपट्टि पहिलो कोठा
    msp.add_line((0, 12), (4.9, 12), dxfattribs={'layer': 'WALLS'})
    msp.add_line((0, 18), (4.9, 18), dxfattribs={'layer': 'WALLS'})
    msp.add_line((0, 24), (4.9, 24), dxfattribs={'layer': 'WALLS'})
    
    msp.add_line((7.1, 10), (12, 10), dxfattribs={'layer': 'WALLS'}) # दायाँपट्टि
    msp.add_line((7.1, 16), (12, 16), dxfattribs={'layer': 'WALLS'})
    msp.add_line((7.1, 22), (12, 22), dxfattribs={'layer': 'WALLS'})

    # ४. ढोका र झ्याल राख्ने (Doors & Windows)
    def add_door(x, y, angle):
        # ढोका कोर्ने (Arc र Line)
        msp.add_line((x, y), (x + math.cos(math.radians(angle))*0.9, y + math.sin(math.radians(angle))*0.9), dxfattribs={'layer': 'DOORS'})
        msp.add_arc((x, y), radius=0.9, start_angle=angle, end_angle=angle+90, dxfattribs={'layer': 'DOORS'})

    def add_window(x1, y1, x2, y2):
        # झ्याल कोर्ने (Double Line)
        msp.add_line((x1, y1), (x2, y2), dxfattribs={'layer': 'WINDOWS'})
        msp.add_line((x1, y1+0.1), (x2, y2+0.1), dxfattribs={'layer': 'WINDOWS'})

    # उदाहरणको लागि केही ढोका र झ्याल
    add_door(4.9, 5, 0)   # करिडोरको ढोका
    add_door(7.1, 15, 180) # अर्को कोठाको ढोका
    add_window(1, 0, 3, 0) # अगाडिको झ्याल
    add_window(8, 30, 11, 30) # पछाडिको झ्याल

    # ५. कोठाको नाम र साइज लेख्ने (Text & Dimensions)
    def add_text(text, x, y, height=0.4):
        msp.add_text(text, dxfattribs={'layer': 'TEXT', 'height': height}).set_placement((x, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    add_text("LIVING ROOM\n4.9m x 8m", 2.45, 4)
    add_text("KITCHEN\n4.9m x 4m", 2.45, 10)
    add_text("BEDROOM 1\n4.9m x 6m", 2.45, 15)
    add_text("BATHROOM\n4.9m x 6m", 2.45, 21)
    add_text("STAIRCASE\n2.2m x 15m", 6.0, 15) # करिडोर सँगै सिँढी
    add_text("BEDROOM 2\n4.9m x 10m", 9.55, 5)
    add_text("BEDROOM 3\n4.9m x 6m", 9.55, 13)
    add_text("BALCONY\n4.9m x 8m", 9.55, 26)

    # ६. नाप (Dimensions)
    # जग्गाको कुल नाप
    msp.add_linear_dim(base=(0, -2), p1=(0, 0), p2=(12, 0), dxfattribs={'layer': 'DIMENSIONS'}).render()
    msp.add_linear_dim(base=(-2, 0), p1=(0, 0), p2=(0, 30), angle=90, dxfattribs={'layer': 'DIMENSIONS'}).render()

    # ७. सेभ गर्ने
    filepath = r"C:\Users\Msi\AIBrain\designs\Nepal_Municipality_Blueprint.dxf"
    doc.saveas(filepath)
    print(f"✅ वास्तविक CAD ब्लुप्रिन्ट तयार भयो: {filepath}")

if __name__ == "__main__":
    create_municipality_blueprint()
