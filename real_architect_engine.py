import ezdxf
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_real_cad():
    # १. कोठाहरूको डेटा (Shared Walls को लागि Coordinates मिलाइएको)
    # (नाम, X, Y, चौडाइ, लम्बाइ, रङ)
    rooms = [
        # Ground Floor (F1)
        ("LIVING", 0, 0, 6, 8, "#a8e6cf"),
        ("KITCHEN", 0, 8, 6, 4, "#ffd3b6"),
        ("STAIRCASE", 0, 12, 3, 4, "#dfe6e9"),
        ("BATH", 3, 12, 3, 4, "#ffaaa5"),
        ("PARKING", 0, 16, 6, 6, "#f8f9fa"),
        ("PUJA", 0, 22, 4, 4, "#ffeaa7"),
        ("BEDROOM 1", 6, 0, 6, 6, "#dcedc1"),
        ("BEDROOM 2", 6, 6, 6, 6, "#dcedc1"),
        ("CORRIDOR", 6, 12, 2, 14, "#e0e0e0"), # लामो करिडोर
        ("BEDROOM 3", 8, 12, 4, 7, "#dcedc1"),
        ("BEDROOM 4", 8, 19, 4, 7, "#dcedc1"),
    ]

    # २. DXF फाइल बनाउने (AutoCAD को लागि)
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    for name, x, y, w, l, color in rooms:
        # पर्खाल कोर्ने
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+l), (x, y+l)], close=True)
        # नाम लेख्ने
        text = msp.add_text(name, dxfattribs={'height': 0.5})
        text.dxf.insert = (x + w/2, y + l/2)

    dxf_path = r"C:\Users\Msi\AIBrain\designs\REAL_ARCHITECT_PLAN.dxf"
    doc.saveas(dxf_path)
    print(f"✅ AutoCAD DXF फाइल बन्यो: {dxf_path}")

    # ३. 2D र 3D डिजाइन बनाएर फोटोको रूपमा सेभ गर्ने
    fig = plt.figure(figsize=(15, 7))
    
    # --- 2D Floor Plan ---
    ax1 = fig.add_subplot(121)
    ax1.set_title("Real 2D Floor Plan", fontsize=16, fontweight='bold')
    for name, x, y, w, l, color in rooms:
        rect = patches.Rectangle((x, y), w, l, linewidth=2, edgecolor='black', facecolor=color)
        ax1.add_patch(rect)
        ax1.text(x + w/2, y + l/2, name, ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax1.set_xlim(-1, 13)
    ax1.set_ylim(-1, 31)
    ax1.invert_yaxis() # घरको ढोका तलतिर हुने भएकोले
    ax1.set_aspect('equal')
    
    # --- 3D Isometric View ---
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_title("Real 3D House (With Roof)", fontsize=16, fontweight='bold')
    
    # 3D मा कोठाहरू उचाल्ने
    for name, x, y, w, l, color in rooms:
        # जमिनको तल्लो भाग
        x_pos = [x, x+w, x+w, x, x]
        y_pos = [y, y, y+l, y+l, y]
        z_pos = [0, 0, 0, 0, 0]
        ax2.plot_trisurf(x_pos, y_pos, z_pos, color=color, alpha=0.8, edgecolor='black')
        
        # छत (Roof) - सबै कोठाको माथि एउटै छाना
        z_roof = [3, 3, 3, 3, 3]
        ax2.plot_trisurf(x_pos, y_pos, z_roof, color='#bdc3c7', alpha=0.5, edgecolor='black')

    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 30)
    ax2.set_zlim(0, 5)
    ax2.view_init(elev=40, azim=-45) # 3D एंगल

    plt.tight_layout()
    img_path = r"C:\Users\Msi\AIBrain\designs\REAL_ARCHITECT_3D.png"
    plt.savefig(img_path, dpi=150, bbox_inches='tight')
    print(f"✅ 2D र 3D फोटो बन्यो: {img_path}")
    
    # फोटो खोल्ने
    import os
    os.startfile(img_path)

if __name__ == "__main__":
    create_real_cad()
