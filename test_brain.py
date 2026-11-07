import ollama
import json
from ddgs import DDGS

def test_ollama_connection():
    print("\n🧠 TEST 1: Testing Ollama Connection...")
    try:
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': 'Say "Kishan AI is online" in Nepali.'}])
        print("✅ AI Reply:", response['message']['content'])
    except Exception as e:
        print("❌ AI Connection Failed:", e)

def test_web_search():
    print("\n🌐 TEST 2: Testing Web Search (Nepal Building Codes)...")
    try:
        results = DDGS().text("Nepal municipality building bylaws setbacks FAR", max_results=1)
        if results:
            print("✅ Search Result Found:", results[0]['title'])
            print("   Snippet:", results[0]['body'][:150] + "...")
        else:
            print("⚠️ Search returned empty.")
    except Exception as e:
        print("❌ Web Search Failed:", e)

def test_5_layouts():
    print("\n📐 TEST 3: Testing AI for 5 Distinct Layouts (JSON)...")
    prompt = """
    You are an architect. Design 5 DIFFERENT 2BHK layouts for a 30x40 site.
    Return ONLY a JSON array containing 5 objects. 
    Each object must have a "title" and a "rooms" list.
    Rooms must have "name", "x", "y", "w", "h".
    Do not overlap rooms.
    Format:
    [
      {"title": "Option A", "rooms": [{"name": "Living", "x": 0, "y": 0, "w": 15, "h": 12}]},
      {"title": "Option B", "rooms": [{"name": "Living", "x": 0, "y": 0, "w": 12, "h": 15}]}
    ]
    """
    try:
        response = ollama.chat(
            model='llama3', 
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
        data = json.loads(response['message']['content'])
        
        # जाँच्ने कि ५ वटा छन् कि छैनन्
        if isinstance(data, dict):
            # यदि AI ले {"designs": [...]} भनेर दियो भने
            for key in data:
                if isinstance(data[key], list):
                    data = data[key]
                    break
        
        if isinstance(data, list) and len(data) == 5:
            print("✅ SUCCESS! AI generated exactly 5 designs.")
            for i, d in enumerate(data):
                print(f"   Option {i+1}: {d.get('title', 'Untitled')} ({len(d.get('rooms', []))} rooms)")
        else:
            print(f"⚠️ FAILED: AI returned {len(data) if isinstance(data, list) else 'invalid'} designs instead of 5.")
            print("Raw Output:", str(data)[:200])
            
    except Exception as e:
        print("❌ Layout Generation Failed:", e)

if __name__ == "__main__":
    print("========================================")
    print("🚀 KISHAN AI - CORE BRAIN DIAGNOSTICS")
    print("========================================")
    test_ollama_connection()
    test_web_search()
    test_5_layouts()
    print("\n========================================")