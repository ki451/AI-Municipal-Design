# ==========================================
# 🧮 PURE MATH TEST (Fixed Overlap)
# ==========================================

def calculate_plan(site_length, site_width):
    print(f"\n{'='*55}")
    print(f"🏠 जग्गा: {site_length} ft (लम्बाई) x {site_width} ft (चौडाई)")
    print(f"{'='*55}")
    
    build_l = site_length - 8
    build_w = site_width - 6
    
    print(f"\n📐 चरण १: सेटब्याक काटियो")
    print(f"   Buildable Length = {site_length} - 8 = {build_l} ft")
    print(f"   Buildable Width  = {site_width} - 6 = {build_w} ft")
    
    rooms = []
    
    # 1. बैठक (Living Room)
    living_h = round(build_l * 0.4, 2)
    rooms.append({"name": "बैठक", "x": 3, "y": 5, "w": round(build_w, 2), "h": living_h})
    
    # 2. करिडोर (Corridor)
    corridor_w = 3.5
    corridor_x = round(3 + (build_w / 2) - (corridor_w / 2), 2)
    corridor_y = round(5 + living_h, 2)
    corridor_h = round(build_l - living_h, 2)
    rooms.append({"name": "कोरिडोर", "x": corridor_x, "y": corridor_y, "w": corridor_w, "h": corridor_h})
    
    # 3. Left Side (2 Bedrooms)
    side_w = round((build_w / 2) - (corridor_w / 2), 2)
    bed_h = round(corridor_h / 2, 2)
    
    rooms.append({"name": "सुत्ने कोठा १", "x": 3, "y": corridor_y, "w": side_w, "h": bed_h})
    rooms.append({"name": "सुत्ने कोठा २", "x": 3, "y": round(corridor_y + bed_h, 2), "w": side_w, "h": bed_h})
    
    # 4. Right Side (Kitchen, Bath, Puja) - FIXED OVERLAP
    right_x = round(3 + (build_w / 2) + (corridor_w / 2), 2)
    
    puja_h = round(corridor_h * 0.2, 2)
    bath_h = round(corridor_h * 0.25, 2)
    kitchen_h = round(corridor_h - puja_h - bath_h, 2) # बाँकी ठाउँ
    
    # अब क्रमशः तलदेखि माथि राख्ने (Overlap नहुने गरी)
    rooms.append({"name": "भान्सा", "x": right_x, "y": corridor_y, "w": side_w, "h": kitchen_h})
    rooms.append({"name": "बाथरुम", "x": right_x, "y": round(corridor_y + kitchen_h, 2), "w": side_w, "h": bath_h})
    rooms.append({"name": "पुजा", "x": right_x, "y": round(corridor_y + kitchen_h + bath_h, 2), "w": side_w, "h": puja_h})
    
    # ==========================================
    # 🔍 VALIDATION CHECK
    # ==========================================
    print(f"\n{'='*55}")
    print("🔍 VALIDATION CHECK (Overlap Test):")
    print(f"{'='*55}")
    
    overlap_found = False
    for i in range(len(rooms)):
        for j in range(i+1, len(rooms)):
            r1, r2 = rooms[i], rooms[j]
            # ओभरल्याप जाँच्ने (Floating point error हटाउन -0.01 को टोलरेन्स)
            if (r1["x"] < r2["x"] + r2["w"] - 0.01 and
                r1["x"] + r1["w"] > r2["x"] + 0.01 and
                r1["y"] < r2["y"] + r2["h"] - 0.01 and
                r1["y"] + r1["h"] > r2["y"] + 0.01):
                print(f"   ❌ OVERLAP: {r1['name']} ↔ {r2['name']}")
                overlap_found = True
    
    if not overlap_found:
        print(f"   ✅ कुनै कोठा ओभरल्याप छैन! Design is CLEAN.")
    
    # ==========================================
    # 📋 FINAL RESULTS
    # ==========================================
    print(f"\n{'='*55}")
    print("📋 FINAL COORDINATES (Python ले हिसाब गरेको):")
    print(f"{'='*55}")
    print(f"{'Room':<18} {'X':>6} {'Y':>6} {'W':>6} {'H':>6}")
    print("-" * 55)
    for r in rooms:
        print(f"{r['name']:<18} {r['x']:>6.2f} {r['y']:>6.2f} {r['w']:>6.2f} {r['h']:>6.2f}")
    
    print(f"\n✅ Total: {len(rooms)} rooms calculated successfully!")
    return rooms

if __name__ == "__main__":
    calculate_plan(30, 40)
    print("\n\n")
    calculate_plan(25, 35)