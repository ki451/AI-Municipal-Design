import os
import requests
import json

API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")




def get_local_fallback():
    print("⚠️ गुगल सर्भर बिजी छ। स्थानीय आर्किटेक्ट ब्रेन (Local Fallback) प्रयोग गर्दै...")
    return [
        {"title": "Standard Plan", "rooms": [{"name": "LIVING", "x": 0, "y": 0, "w": 6, "h": 8}, {"name": "KITCHEN", "x": 0, "y": 8, "w": 6, "h": 4}, {"name": "STAIR", "x": 0, "y": 12, "w": 3, "h": 4}, {"name": "BATH", "x": 3, "y": 12, "w": 3, "h": 4}, {"name": "BED 1", "x": 6, "y": 0, "w": 6, "h": 6}, {"name": "BED 2", "x": 6, "y": 6, "w": 6, "h": 6}, {"name": "CORRIDOR", "x": 6, "y": 12, "w": 2, "h": 18}, {"name": "BED 3", "x": 8, "y": 12, "w": 4, "h": 9}, {"name": "BED 4", "x": 8, "y": 21, "w": 4, "h": 9}]},
        {"title": "Central Corridor", "rooms": [{"name": "CORRIDOR", "x": 5, "y": 0, "w": 2, "h": 30}, {"name": "LIVING", "x": 0, "y": 0, "w": 5, "h": 10}, {"name": "DINING", "x": 0, "y": 10, "w": 5, "h": 6}, {"name": "KITCHEN", "x": 0, "y": 16, "w": 5, "h": 5}, {"name": "STAIR", "x": 0, "y": 21, "w": 5, "h": 9}, {"name": "BED 1", "x": 7, "y": 0, "w": 5, "h": 8}, {"name": "BATH", "x": 7, "y": 8, "w": 5, "h": 4}, {"name": "BED 2", "x": 7, "y": 12, "w": 5, "h": 8}, {"name": "BED 3", "x": 7, "y": 20, "w": 5, "h": 6}, {"name": "PUJA", "x": 7, "y": 26, "w": 5, "h": 4}]},
        {"title": "Courtyard Focus", "rooms": [{"name": "CORRIDOR", "x": 0, "y": 10, "w": 12, "h": 2}, {"name": "LIVING", "x": 0, "y": 0, "w": 8, "h": 10}, {"name": "STAIR", "x": 8, "y": 0, "w": 4, "h": 5}, {"name": "BATH", "x": 8, "y": 5, "w": 4, "h": 5}, {"name": "KITCHEN", "x": 0, "y": 12, "w": 5, "h": 8}, {"name": "BED 1", "x": 5, "y": 12, "w": 7, "h": 8}, {"name": "BED 2", "x": 0, "y": 20, "w": 6, "h": 10}, {"name": "BED 3", "x": 6, "y": 20, "w": 6, "h": 6}, {"name": "PUJA", "x": 6, "y": 26, "w": 6, "h": 4}]},
        {"title": "Open Plan", "rooms": [{"name": "LIVING + DINING", "x": 0, "y": 0, "w": 7, "h": 12}, {"name": "KITCHEN", "x": 7, "y": 0, "w": 5, "h": 6}, {"name": "STAIR + BATH", "x": 7, "y": 6, "w": 5, "h": 6}, {"name": "BED 1", "x": 0, "y": 12, "w": 7, "h": 6}, {"name": "BED 2", "x": 7, "y": 12, "w": 5, "h": 6}, {"name": "BED 3", "x": 0, "y": 18, "w": 7, "h": 6}, {"name": "BED 4", "x": 7, "y": 18, "w": 5, "h": 6}, {"name": "BALCONY", "x": 0, "y": 24, "w": 12, "h": 6}]},
        {"title": "Compact Core", "rooms": [{"name": "LIVING", "x": 0, "y": 0, "w": 12, "h": 8}, {"name": "KITCHEN", "x": 0, "y": 8, "w": 4, "h": 5}, {"name": "CORRIDOR", "x": 4, "y": 8, "w": 2, "h": 22}, {"name": "BATH", "x": 6, "y": 8, "w": 3, "h": 5}, {"name": "STAIR", "x": 9, "y": 8, "w": 3, "h": 5}, {"name": "BED 1", "x": 0, "y": 13, "w": 4, "h": 6}, {"name": "BED 2", "x": 6, "y": 13, "w": 6, "h": 6}, {"name": "BED 3", "x": 0, "y": 19, "w": 6, "h": 7}, {"name": "PUJA", "x": 6, "y": 19, "w": 6, "h": 7}, {"name": "PARKING", "x": 0, "y": 26, "w": 12, "h": 4}]}
    ]

def ask_ai_architect():
    print("🧠 AI (Architect) ले पूरा घरको डिजाइन सोच्दै...")
    
    prompt = """
    You are an expert architect in Nepal. Design 5 different layout options for a 12m x 30m house.
    Return ONLY a valid JSON array of 5 objects. Each object must have:
    1. "title": "Name of plan"
    2. "rooms": Array of objects with: "name", "x", "y", "w", "h".
    Ensure walls are shared. Include: Living, Kitchen, Bedroom, Bathroom, Staircase, Puja.
    Do not include markdown, only the JSON array.
    """
    
    # ✅ गुगलको सुझाव अनुसार नयाँ मोडेलहरू
    models = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash"]
    
    for model in models:
        print(f"  प्रयास गर्दै: {model}...")
        url_api = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url_api, json=payload, timeout=60)
            data = res.json()
            
            if 'error' in data:
                print(f"  ⚠️ {model} मा समस्या: {data['error']['message']}")
                continue
                
            text = data['candidates'][0]['content']['parts'][0]['text']
            text = text.replace("```json", "").replace("```", "").strip()
            designs = json.loads(text)
            print("✅ AI ले डिजाइन तयार गर्यो!")
            generate_html(designs)
            return
            
        except Exception as e:
            print(f"  ⚠️ {model} मा समस्या: {e}")

    # यदि सबै API फेल भए, स्थानीय ब्रेन प्रयोग गर्ने
    designs = get_local_fallback()
    generate_html(designs)

def generate_html(designs):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Architect Designs</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; padding: 20px; }
            h1 { text-align: center; color: #2c3e50; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h3 { color: #2980b9; text-align: center; }
            svg { display: block; margin: 0 auto; background: #fff; border: 2px solid #bdc3c7; }
            .room { stroke: #2c3e50; stroke-width: 2; }
            .label { font-size: 10px; font-weight: bold; fill: #111; text-anchor: middle; dominant-baseline: middle; }
        </style>
    </head>
    <body>
        <h1>🏗️ Municipality Approved Designs</h1>
        <div class="grid">
    """
    
    count = 1
    for design in designs:
        html += f"<div class='card'><h3>Option {count} : {design.get('title', 'Design')}</h3>"
        html += "<svg width='240' height='600'>"
        
        for room in design.get("rooms", []):
            x = room.get("x", 0) * 20
            y = room.get("y", 0) * 20
            w = room.get("w", 3) * 20
            h = room.get("h", 3) * 20
            name = room.get("name", "Room")
            
            color = "#a8e6cf"
            if "Bed" in name: color = "#dcedc1"
            elif "Kitchen" in name: color = "#ffd3b6"
            elif "Bath" in name: color = "#ffaaa5"
            elif "Puja" in name: color = "#ffeaa7"
            elif "Corridor" in name: color = "#e0e0e0"
            elif "Stair" in name: color = "#dfe6e9"
            
            html += f"<rect x='{x}' y='{y}' width='{w}' height='{h}' class='room' fill='{color}' />"
            html += f"<text x='{x + w/2}' y='{y + h/2}' class='label'>{name}</text>"
            
        html += "</svg></div>"
        count += 1
        
    html += "</div></body></html>"
    
    out_path = "C:\\Users\\Msi\\AIBrain\\designs\\AI_Architect_5_Designs.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"🎉 डिजाइन तयार भयो: {out_path}")
    os.startfile(out_path)

if __name__ == "__main__":
    ask_ai_architect()
