import os

def create_3d_obj():
    rooms = [
        {"name": "LIVING", "x": 0, "y": 0, "w": 6, "h": 8},
        {"name": "FAMILY", "x": 0, "y": 8, "w": 6, "h": 8},
        {"name": "BED 1", "x": 0, "y": 16, "w": 6, "h": 7},
        {"name": "KITCHEN", "x": 0, "y": 23, "w": 6, "h": 7},
        {"name": "STAIR", "x": 6, "y": 0, "w": 6, "h": 8},
        {"name": "PUJA", "x": 6, "y": 8, "w": 3, "h": 8},
        {"name": "BATH", "x": 9, "y": 8, "w": 3, "h": 8},
        {"name": "BED 2", "x": 6, "y": 16, "w": 6, "h": 7},
        {"name": "DINING", "x": 6, "y": 23, "w": 6, "h": 7}
    ]
    
    wall_height = 3.0 # प्रत्येक तल्लाको उचाइ (3 मिटर)
    floors = 3       # ३ तल्ला

    vertices = []
    faces = []
    
    # Vertex थप्ने फंक्शन
    def add_vertex(x, y, z):
        vertices.append((x, y, z))
        return len(vertices)  # 1-based index for OBJ
        
    # Quad (4 point) फेस थप्ने फंक्शन
    def add_face(v1, v2, v3, v4):
        faces.append((v1, v2, v3, v4))

    # प्रत्येक कोठाको लागि 3D बक्स बनाउने
    for r in rooms:
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        
        for f in range(floors):
            z1 = f * wall_height
            z2 = (f + 1) * wall_height
            
            # 8 corners of the 3D box
            v1 = add_vertex(x, y, z1)
            v2 = add_vertex(x+w, y, z1)
            v3 = add_vertex(x+w, y+h, z1)
            v4 = add_vertex(x, y+h, z1)
            v5 = add_vertex(x, y, z2)
            v6 = add_vertex(x+w, y, z2)
            v7 = add_vertex(x+w, y+h, z2)
            v8 = add_vertex(x, y+h, z2)
            
            # 6 faces (Bottom, Top, Front, Back, Left, Right)
            add_face(v1, v2, v3, v4) # Bottom
            add_face(v5, v6, v7, v8) # Top
            add_face(v1, v2, v6, v5) # Front
            add_face(v2, v3, v7, v6) # Right
            add_face(v3, v4, v8, v7) # Back
            add_face(v4, v1, v5, v8) # Left

    # OBJ फाइल बनाउने
    out_dir = r"C:\Users\Msi\AIBrain\designs"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    filepath = os.path.join(out_dir, "Kishan_AI_3D_House.obj")
    
    with open(filepath, 'w') as f:
        # Vertex लेख्ने
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        # Face लेख्ने
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")
            
    print(f"✅ 3D मोडेल (OBJ) तयार भयो: {filepath}")
    os.startfile(out_dir)

if __name__ == "__main__":
    create_3d_obj()
