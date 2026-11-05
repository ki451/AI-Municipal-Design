import ezdxf

def create_real_house_layout():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # नगरपालिकाको मापदण्ड अनुसार वास्तविक घरको लेआउट
    # कुल क्षेत्रफल: 12m x 30m
    # बीचमा 2m चौडा र 30m लामो करिडोर
    rooms = [
        # नाम, X1, Y1, X2, Y2, रङ कोड
        ("CORRIDOR", 4.0, 0.0, 6.0, 30.0, 8),
        
        # बायाँ भाग (Left Side)
        ("PARKING", 0.0, 0.0, 4.0, 6.0, 9),
        ("PUJA ROOM", 0.0, 6.0, 4.0, 9.0, 6),
        ("BATHROOM", 0.0, 9.0, 4.0, 12.0, 1),
        ("BEDROOM 1", 0.0, 12.0, 4.0, 18.0, 2),
        ("BEDROOM 2", 0.0, 18.0, 4.0, 24.0, 2),
        ("BALCONY", 0.0, 24.0, 4.0, 30.0, 4),
        
        # दायाँ भाग (Right Side)
        ("LIVING ROOM", 6.0, 0.0, 12.0, 8.0, 3),
        ("KITCHEN", 6.0, 8.0, 12.0, 12.0, 30),
        ("STAIRCASE", 6.0, 12.0, 12.0, 16.0, 4),
        ("BEDROOM 3", 6.0, 16.0, 12.0, 22.0, 2),
        ("BEDROOM 4", 6.0, 22.0, 12.0, 26.0, 2),
        ("BATHROOM 2", 6.0, 26.0, 12.0, 30.0, 1)
    ]

    for name, x1, y1, x2, y2, color in rooms:
        # पर्खाल कोर्ने (Shared Walls)
        msp.add_lwpolyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], close=True, dxfattribs={'color': color})
        
        # कोठाको नाम लेख्ने (सच्याइएको तरिका)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        text = msp.add_text(name, dxfattribs={'height': 0.5, 'color': 7}) 
        text.dxf.insert = (cx, cy) # नयाँ तरिका

    filepath = r"C:\Users\Msi\AIBrain\designs\Real_House_Plan.dxf"
    doc.saveas(filepath)
    print(f"✅ वास्तविक नक्सा तयार भयो: {filepath}")

if __name__ == "__main__":
    create_real_house_layout()
