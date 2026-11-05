import os
import requests
import base64
import json

API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")









def get_real_floor_plan():
    # १. पहिले कम्प्युटरमा भएको तस्बिर खोज्ने (real_plan.jpg)
    local_path = "C:\\Users\\Msi\\real_plan.jpg"
    if os.path.exists(local_path):
        print("Local image found. Using real_plan.jpg")
        with open(local_path, 'rb') as f:
            return f.read()
    
    # २. नभए इन्टरनेटबाट डाउनलोड गर्ने (विकिमिडियाबाट, कहिल्यै ब्लक हुँदैन)
    print("Downloading a real floor plan from Wikimedia...")
    img_url = "https://upload.wikimedia.org/wikipedia/commons/9/9a/Sample_Floorplan.jpg"
    try:
        res = requests.get(img_url, timeout=10)
        if res.status_code == 200:
            return res.content
    except:
        pass
        
    # ३. त्यो पनि भएन भने आफैं तस्बिर बनाउने (कम्तीमा ३ कोठा)
    print("Creating local dummy image with multiple rooms...")
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (800, 600), color='white')
    d = ImageDraw.Draw(img)
    d.rectangle([50, 50, 350, 450], outline="black", width=3) # Bedroom
    d.rectangle([350, 50, 750, 250], outline="black", width=3) # Living
    d.rectangle([350, 250, 550, 450], outline="black", width=3) # Kitchen
    d.text((150, 200), "BEDROOM", fill="black")
    d.text((450, 120), "LIVING", fill="black")
    d.text((400, 320), "KITCHEN", fill="black")
    save_path = "C:\\Users\\Msi\\AIBrain\\dummy_plan_multi.jpg"
    img.save(save_path)
    with open(save_path, 'rb') as f:
        return f.read()

def analyze_plan():
    img_data = get_real_floor_plan()
    print("AI is analyzing the image...")
    
    base64_img = base64.b64encode(img_data).decode('utf-8')
    
    # नगरपालिकाको नियम (NBC) जाँच्ने प्रम्प्ट
    prompt = """
    Analyze this architectural floor plan for a house in Nepal. 
    Return ONLY a valid JSON object:
    { 
      "rooms": [ {"name": "Living", "x": 0, "y": 0, "w": 5, "h": 6}, {"name": "Kitchen", "x": 5, "y": 0, "w": 4, "h": 6} ],
      "bylaw_check": {
        "has_staircase": true,
        "has_puja_room": true,
        "setback_note": "Minimum 1.5m setback required"
      }
    }
    Make sure the rooms fit into a 12x30 envelope. Use shared walls.
    """
    
    models = ["gemini-3.5-flash", "gemini-2.5-flash"] # पहिले नयाँ मोडेल प्रयास गर्ने
    
    for model in models:
        url_api = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": base64_img}}
                ]
            }]
        }
        
        try:
            res = requests.post(url_api, json=payload, timeout=20)
            data = res.json()
            
            if 'error' in data:
                print(f"API Error on {model}: {data['error']['message']}")
                continue
                
            text = data['candidates'][0]['content']['parts'][0]['text']
            text = text.replace("```json", "").replace("```", "").strip()
            design_data = json.loads(text)
            print("Success! Design generated.")
            generate_html(design_data)
            return
            
        except Exception as e:
            print(f"Error on {model}: {e}")

    print("All models failed. Please check API Key.")

def generate_html(data):
    html = """
    <!DOCTYPE html><html><head><title>AI Learned Design</title>
    <style>
        body { font-family: 'Segoe UI'; background: #f4f7f6; padding: 20px; text-align: center; }
        .card { background: white; padding: 20px; display: inline-block; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        svg { border: 2px solid #bdc3c7; background: #fff; }
        .room { stroke: #333; stroke-width: 2; fill: #a8e6cf; }
        .label { font-size: 12px; font-weight: bold; fill: #111; text-anchor: middle; dominant-baseline: middle; }
        .info { margin-top: 20px; text-align: left; background: #e8f4f8; padding: 10px; border-radius: 5px; }
    </style></head><body>
    <div class="card"><h2>AI Generated Design (Learned from Internet)</h2>
    <svg width="300" height="750">
    """
    
    for room in data.get("rooms", []):
        x = room.get("x", 0) * 25
        y = room.get("y", 0) * 25
        w = room.get("w", 3) * 25
        h = room.get("h", 3) * 25
        name = room.get("name", "Room")
        
        html += f"<rect x='{x}' y='{y}' width='{w}' height='{h}' class='room' />"
        html += f"<text x='{x + w/2}' y='{y + h/2}' class='label'>{name}</text>"
        
    html += "</svg>"
    
    # नगरपालिका जाँच रिपोर्ट देखाउने
    bylaw = data.get("bylaw_check", {})
    if bylaw:
        html += f"<div class='info'><h3>Municipality Check:</h3>"
        html += f"<p>Staircase: {'✅' if bylaw.get('has_staircase') else '❌'}</p>"
        html += f"<p>Puja Room: {'✅' if bylaw.get('has_puja_room') else '❌'}</p>"
        html += f"<p>Setback: {bylaw.get('setback_note', 'N/A')}</p></div>"
    
    html += "</div></body></html>"
    
    out_path = "C:\\Users\\Msi\\AIBrain\\designs\\AI_Learned_Design.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Design saved to: {out_path}")
    os.startfile(out_path)

if __name__ == "__main__":
    analyze_plan()
