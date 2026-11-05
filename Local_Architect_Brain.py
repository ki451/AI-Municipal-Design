import os

def generate_designs():
    out_dir = r"C:\Users\Msi\AIBrain\designs"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    # ५ वटा डिजाइनको डेटा (पर्खाल जोडिएका, कुनै खाली ठाउँ छैन)
    designs = [
        {
            "title": "1. Standard Plan (Front Living)",
            "rooms": [
                {"n": "LIVING", "x": 0, "y": 0, "w": 6, "h": 8, "c": "#a8e6cf"},
                {"n": "KITCHEN", "x": 0, "y": 8, "w": 6, "h": 4, "c": "#ffd3b6"},
                {"n": "STAIR", "x": 0, "y": 12, "w": 3, "h": 4, "c": "#dfe6e9"},
                {"n": "BATH", "x": 3, "y": 12, "w": 3, "h": 4, "c": "#ffaaa5"},
                {"n": "PARKING", "x": 0, "y": 16, "w": 6, "h": 6, "c": "#f8f9fa"},
                {"n": "PUJA", "x": 0, "y": 22, "w": 4, "h": 4, "c": "#ffeaa7"},
                {"n": "BED 1", "x": 6, "y": 0, "w": 6, "h": 6, "c": "#dcedc1"},
                {"n": "BED 2", "x": 6, "y": 6, "w": 6, "h": 6, "c": "#dcedc1"},
                {"n": "CORRIDOR", "x": 6, "y": 12, "w": 2, "h": 18, "c": "#e0e0e0"},
                {"n": "BED 3", "x": 8, "y": 12, "w": 4, "h": 9, "c": "#dcedc1"},
                {"n": "BED 4", "x": 8, "y": 21, "w": 4, "h": 9, "c": "#dcedc1"},
            ],
            "doors": [(3,8), (1.5,12), (6,8), (7,14)],
            "windows": [(1,0,4,0), (1,16,4,16), (7,0,10,0), (9,30,11,30)]
        },
        {
            "title": "2. Central Corridor",
            "rooms": [
                {"n": "CORRIDOR", "x": 5, "y": 0, "w": 2, "h": 30, "c": "#e0e0e0"},
                {"n": "LIVING", "x": 0, "y": 0, "w": 5, "h": 10, "c": "#a8e6cf"},
                {"n": "DINING", "x": 0, "y": 10, "w": 5, "h": 6, "c": "#ffeaa7"},
                {"n": "KITCHEN", "x": 0, "y": 16, "w": 5, "h": 5, "c": "#ffd3b6"},
                {"n": "STAIR", "x": 0, "y": 21, "w": 5, "h": 9, "c": "#dfe6e9"},
                {"n": "BED 1", "x": 7, "y": 0, "w": 5, "h": 8, "c": "#dcedc1"},
                {"n": "BATH", "x": 7, "y": 8, "w": 5, "h": 4, "c": "#ffaaa5"},
                {"n": "BED 2", "x": 7, "y": 12, "w": 5, "h": 8, "c": "#dcedc1"},
                {"n": "BED 3", "x": 7, "y": 20, "w": 5, "h": 6, "c": "#dcedc1"},
                {"n": "PUJA", "x": 7, "y": 26, "w": 5, "h": 4, "c": "#ffeaa7"}
            ],
            "doors": [(5,5), (7,2), (7,10), (7,15)],
            "windows": [(1,0,3,0), (7,0,10,0), (7,12,10,12)]
        },
        {
            "title": "3. Courtyard Focus",
            "rooms": [
                {"n": "CORRIDOR", "x": 0, "y": 10, "w": 12, "h": 2, "c": "#e0e0e0"},
                {"n": "LIVING", "x": 0, "y": 0, "w": 8, "h": 10, "c": "#a8e6cf"},
                {"n": "STAIR", "x": 8, "y": 0, "w": 4, "h": 5, "c": "#dfe6e9"},
                {"n": "BATH", "x": 8, "y": 5, "w": 4, "h": 5, "c": "#ffaaa5"},
                {"n": "KITCHEN", "x": 0, "y": 12, "w": 5, "h": 8, "c": "#ffd3b6"},
                {"n": "BED 1", "x": 5, "y": 12, "w": 7, "h": 8, "c": "#dcedc1"},
                {"n": "BED 2", "x": 0, "y": 20, "w": 6, "h": 10, "c": "#dcedc1"},
                {"n": "BED 3", "x": 6, "y": 20, "w": 6, "h": 6, "c": "#dcedc1"},
                {"n": "PUJA", "x": 6, "y": 26, "w": 6, "h": 4, "c": "#ffeaa7"}
            ],
            "doors": [(2,10), (6,10), (3,12), (7,12)],
            "windows": [(2,0,6,0), (7,20,9,20)]
        },
        {
            "title": "4. Open Plan",
            "rooms": [
                {"n": "LIVING + DINING", "x": 0, "y": 0, "w": 7, "h": 12, "c": "#a8e6cf"},
                {"n": "KITCHEN", "x": 7, "y": 0, "w": 5, "h": 6, "c": "#ffd3b6"},
                {"n": "STAIR + BATH", "x": 7, "y": 6, "w": 5, "h": 6, "c": "#dfe6e9"},
                {"n": "BED 1", "x": 0, "y": 12, "w": 7, "h": 6, "c": "#dcedc1"},
                {"n": "BED 2", "x": 7, "y": 12, "w": 5, "h": 6, "c": "#dcedc1"},
                {"n": "BED 3", "x": 0, "y": 18, "w": 7, "h": 6, "c": "#dcedc1"},
                {"n": "BED 4", "x": 7, "y": 18, "w": 5, "h": 6, "c": "#dcedc1"},
                {"n": "BALCONY", "x": 0, "y": 24, "w": 12, "h": 6, "c": "#81ecec"}
            ],
            "doors": [(7,2), (7,8), (3,12), (7,15)],
            "windows": [(1,0,5,0), (1,18,5,18), (2,30,10,30)]
        },
        {
            "title": "5. Compact Core",
            "rooms": [
                {"n": "LIVING", "x": 0, "y": 0, "w": 12, "h": 8, "c": "#a8e6cf"},
                {"n": "KITCHEN", "x": 0, "y": 8, "w": 4, "h": 5, "c": "#ffd3b6"},
                {"n": "CORRIDOR", "x": 4, "y": 8, "w": 2, "h": 22, "c": "#e0e0e0"},
                {"n": "BATH", "x": 6, "y": 8, "w": 3, "h": 5, "c": "#ffaaa5"},
                {"n": "STAIR", "x": 9, "y": 8, "w": 3, "h": 5, "c": "#dfe6e9"},
                {"n": "BED 1", "x": 0, "y": 13, "w": 4, "h": 6, "c": "#dcedc1"},
                {"n": "BED 2", "x": 6, "y": 13, "w": 6, "h": 6, "c": "#dcedc1"},
                {"n": "BED 3", "x": 0, "y": 19, "w": 6, "h": 7, "c": "#dcedc1"},
                {"n": "PUJA", "x": 6, "y": 19, "w": 6, "h": 7, "c": "#ffeaa7"},
                {"n": "PARKING", "x": 0, "y": 26, "w": 12, "h": 4, "c": "#f8f9fa"}
            ],
            "doors": [(2,8), (5,8), (7,8), (2,13), (7,13)],
            "windows": [(2,0,9,0), (1,19,4,19)]
        }
    ]

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kishan AI - Municipality Designs</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #eef2f5; padding: 20px; }
            h1 { text-align: center; color: #2c3e50; margin-bottom: 30px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
            .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            h3 { text-align: center; color: #2980b9; margin-bottom: 15px; font-size: 16px; }
            svg { display: block; margin: 0 auto; background: #fff; border: 2px solid #bdc3c7; border-radius: 5px; }
            .room { stroke: #2c3e50; stroke-width: 2; }
            .door { stroke: #8e44ad; stroke-width: 3; fill: none; }
            .window { stroke: #3498db; stroke-width: 5; }
            .label { font-size: 10px; font-weight: bold; fill: #111; text-anchor: middle; dominant-baseline: middle; }
        </style>
    </head>
    <body>
        <h1>🏗️ 5 Complete Municipality Designs</h1>
        <div class="grid">
    """

    for d in designs:
        html += f"<div class='card'><h3>{d['title']}</h3><svg width='240' height='600'>"
        
        # Rooms
        for r in d["rooms"]:
            px, py, pw, ph = r["x"]*20, r["y"]*20, r["w"]*20, r["h"]*20
            html += f"<rect x='{px}' y='{py}' width='{pw}' height='{ph}' class='room' fill='{r['c']}' />"
            html += f"<text x='{px + pw/2}' y='{py + ph/2}' class='label'>{r['n']}</text>"
            
        # Doors (Arc representation)
        for dr in d["doors"]:
            dx, dy = dr[0]*20, dr[1]*20
            html += f"<path d='M {dx} {dy} A 15 15 0 0 1 {dx+15} {dy-15}' class='door' />"
            
        # Windows (Lines)
        for w in d["windows"]:
            x1, y1, x2, y2 = w[0]*20, w[1]*20, w[2]*20, w[3]*20
            html += f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' class='window' />"
            
        html += "</svg></div>"
        
    html += "</div></body></html>"

    out_file = os.path.join(out_dir, "Final_5_Designs.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ ५ वटा डिजाइन तयार भए: {out_file}")
    os.startfile(out_file)

if __name__ == "__main__":
    generate_designs()
