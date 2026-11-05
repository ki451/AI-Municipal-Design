import os

def generate_complete_design():
    # डिजाइनको डेटा (१२x३० को घर)
    rooms = [
        {"name": "LIVING", "x": 0, "y": 0, "w": 6, "h": 8, "color": "#a8e6cf"},
        {"name": "FAMILY", "x": 0, "y": 8, "w": 6, "h": 8, "color": "#dcedc1"},
        {"name": "BED 1", "x": 0, "y": 16, "w": 6, "h": 7, "color": "#dcedc1"},
        {"name": "KITCHEN", "x": 0, "y": 23, "w": 6, "h": 7, "color": "#ffd3b6"},
        {"name": "STAIR", "x": 6, "y": 0, "w": 6, "h": 8, "color": "#dfe6e9"},
        {"name": "PUJA", "x": 6, "y": 8, "w": 3, "h": 8, "color": "#ffeaa7"},
        {"name": "BATH", "x": 9, "y": 8, "w": 3, "h": 8, "color": "#ffaaa5"},
        {"name": "BED 2", "x": 6, "y": 16, "w": 6, "h": 7, "color": "#dcedc1"},
        {"name": "DINING", "x": 6, "y": 23, "w": 6, "h": 7, "color": "#a8e6cf"}
    ]

    # HTML र Three.js (3D) कोड
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Complete Municipality Design</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; margin: 0; padding: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { color: #2c3e50; margin: 0; }
            .header p { color: #7f8c8d; }
            .container { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
            .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
            .card h2 { color: #2980b9; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; margin-top: 0; font-size: 18px; }
            
            /* 3D Container */
            #3d-view { width: 100%; height: 400px; background: #2c3e50; border-radius: 8px; overflow: hidden; position: relative; }
            
            /* 2D SVG */
            svg { width: 100%; height: auto; border: 2px solid #bdc3c7; background: #fff; }
            .room { stroke: #2c3e50; stroke-width: 2; }
            .label { font-size: 12px; font-weight: bold; fill: #111; text-anchor: middle; dominant-baseline: middle; }
            
            .print-btn { display: block; width: 100%; padding: 15px; background: #27ae60; color: white; text-align: center; font-weight: bold; border: none; border-radius: 8px; margin-top: 30px; cursor: pointer; font-size: 16px; }
            .print-btn:hover { background: #219150; }
            
            @media print {
                body { background: white; padding: 0; }
                .print-btn { display: none; }
                .container { display: block; }
                .card { box-shadow: none; page-break-inside: avoid; margin-bottom: 20px; border: 1px solid #ccc; }
                #3d-view { display: none; } /* 3D प्रिन्ट हुँदैन, तर 2D प्लानहरू प्रिन्ट हुन्छन् */
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏗️ Municipality Approved Design</h1>
            <p>12m x 30m Residential Building</p>
        </div>
        <div class="container">
            <!-- 3D View -->
            <div class="card" style="grid-column: 1 / -1;">
                <h2>3D Interactive View (Rotate & Zoom)</h2>
                <div id="3d-view"></div>
            </div>

            <!-- Floor Plan -->
            <div class="card">
                <h2>1. Ground Floor Plan</h2>
                <svg viewBox="-2 -2 16 34">
    """
    
    # 2D Floor Plan Draw गर्ने
    for r in rooms:
        html += f'<rect x="{r["x"]}" y="{r["y"]}" width="{r["w"]}" height="{r["h"]}" class="room" fill="{r["color"]}" />'
        html += f'<text x="{r["x"] + r["w"]/2}" y="{r["y"] + r["h"]/2}" class="label">{r["name"]}</text>'
    
    html += """
                </svg>
            </div>

            <!-- Structural Layout -->
            <div class="card">
                <h2>2. Structural Layout (Columns & Beams)</h2>
                <svg viewBox="-2 -2 16 34">
                    <rect x="0" y="0" width="12" height="30" fill="none" stroke="#333" stroke-width="2" />
    """
    # पिलरहरू (Columns) राख्ने
    for x in [0, 6, 12]:
        for y in [0, 8, 16, 23, 30]:
            html += f'<rect x="{x-0.2}" y="{y-0.2}" width="0.4" height="0.4" fill="#e74c3c" />'
    
    html += """
                </svg>
                <p style="font-size:12px; color:#7f8c8d; text-align:center;">Red boxes indicate RCC Columns (9"x9")</p>
            </div>
            
            <!-- Elevation -->
            <div class="card" style="grid-column: 1 / -1;">
                <h2>3. Front Elevation (3 Floors)</h2>
                <svg viewBox="-2 -2 16 16">
                    <rect x="0" y="0" width="12" height="12" fill="#f8f9fa" stroke="#333" stroke-width="1" />
                    <!-- Ground Floor -->
                    <rect x="1" y="0" width="2" height="3" fill="#a8e6cf" />
                    <rect x="9" y="0" width="2" height="3" fill="#a8e6cf" />
                    <rect x="5" y="0" width="2" height="4" fill="#ffd3b6" /> <!-- Main Door -->
                    <!-- First Floor -->
                    <rect x="1" y="4" width="2" height="3" fill="#a8e6cf" />
                    <rect x="9" y="4" width="2" height="3" fill="#a8e6cf" />
                    <rect x="5" y="4" width="2" height="3" fill="#a8e6cf" />
                    <!-- Second Floor -->
                    <rect x="1" y="8" width="2" height="3" fill="#a8e6cf" />
                    <rect x="9" y="8" width="2" height="3" fill="#a8e6cf" />
                    <rect x="5" y="8" width="2" height="3" fill="#a8e6cf" />
                    <!-- Roof -->
                    <rect x="0" y="11" width="12" height="1" fill="#333" />
                </svg>
            </div>
        </div>
        
        <button class="print-btn" onclick="window.print()">🖨️ Print to PDF (Save for Municipality)</button>

        <script>
            // 3D View Logic (Three.js)
            const container = document.getElementById('3d-view');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x2c3e50);
            
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(15, 20, 30);
            camera.lookAt(6, 0, 15);

            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight.position.set(10, 20, 10);
            scene.add(dirLight);

            const roomsData = """ + str(rooms).replace("'", '"') + """;
            const wallHeight = 3.0;

            roomsData.forEach(r => {
                const w = r.w;
                const h = r.h;
                const x = r.x + w/2;
                const z = r.y + h/2;
                
                // Room Box
                const geo = new THREE.BoxGeometry(w, wallHeight, h);
                const mat = new THREE.MeshPhongMaterial({ color: new THREE.Color(r.color), transparent: true, opacity: 0.9 });
                const mesh = new THREE.Mesh(geo, mat);
                mesh.position.set(x, wallHeight/2, z);
                scene.add(mesh);
                
                // Edges
                const edges = new THREE.EdgesGeometry(geo);
                const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x333333 }));
                line.position.copy(mesh.position);
                scene.add(line);
            });

            // Mouse rotation logic
            let isDragging = false;
            let previousMousePosition = { x: 0, y: 0 };
            
            renderer.domElement.addEventListener('mousedown', e => { isDragging = true; });
            renderer.domElement.addEventListener('mouseup', e => { isDragging = false; });
            renderer.domElement.addEventListener('mousemove', e => {
                if(isDragging) {
                    const deltaMove = { x: e.offsetX - previousMousePosition.x, y: e.offsetY - previousMousePosition.y };
                    const rotationSpeed = 0.01;
                    // Simple orbit simulation
                    const radius = Math.sqrt(camera.position.x**2 + camera.position.z**2);
                    let theta = Math.atan2(camera.position.x, camera.position.z);
                    let phi = Math.acos(camera.position.y / radius);
                    
                    theta -= deltaMove.x * rotationSpeed;
                    phi -= deltaMove.y * rotationSpeed;
                    
                    phi = Math.max(0.1, Math.min(Math.PI/2 - 0.1, phi)); // Prevent flipping
                    
                    camera.position.x = radius * Math.sin(phi) * Math.sin(theta);
                    camera.position.z = radius * Math.sin(phi) * Math.cos(theta);
                    camera.position.y = radius * Math.cos(phi);
                    camera.lookAt(6, 0, 15);
                }
                previousMousePosition = { x: e.offsetX, y: e.offsetY };
            });

            function animate() {
                requestAnimationFrame(animate);
                renderer.render(scene, camera);
            }
            animate();
            
            // Resize handler
            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
        </script>
    </body>
    </html>
    """

    out_dir = r"C:\Users\Msi\AIBrain\designs"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    filepath = os.path.join(out_dir, "Municipality_Complete_Design.html")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"✅ सफल! पूरा डिजाइन तयार भयो: {filepath}")
    os.startfile(filepath)

if __name__ == "__main__":
    generate_complete_design()
