import argparse
import webbrowser
import os
from .core import s
from .encrypt import encrypt
from rgbprint import gradient_print, Color
from flask import Flask

html_sc = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FiveTemp</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            height: 100%;
            overflow: hidden;
        }
        #background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }
        .container {
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .title {
            text-align: center;
            font-size: 4em;
            font-weight: bold;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 20px;
            background: linear-gradient(45deg, #8c5cf7, #5c8cf7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from {
                text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #8c5cf7, 0 0 20px #8c5cf7;
            }
            to {
                text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #5c8cf7, 0 0 40px #5c8cf7;
            }
        }
        .menu {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 10px;
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .menu-item {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            margin: 0 10px;
            border-radius: 15px;
            transition: all 0.3s;
        }
        .menu-item:hover, .menu-item.active {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.05);
        }
        .content {
            display: none;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.5s, transform 0.5s;
        }
        .content.active {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }
        .box-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .box {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            width: calc(33.33% - 20px);
            box-sizing: border-box;
            transition: all 0.3s;
            position: relative;
        }
        .box:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        .box h3 {
            color: #f0f0f0;
            margin-top: 0;
            padding-right: 80px;
        }
        .box p {
            color: #d0d0d0;
        }
        .box .date {
            color: #b0b0b0;
            font-size: 0.9em;
            position: absolute;
            top: 20px;
            right: 20px;
        }
        .box button {
            background: #8c5cf7;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .box button:hover {
            background: #7140e0;
            transform: scale(1.05);
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 2;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.4);
            opacity: 0;
            transition: opacity 0.3s;
        }
        .modal.active {
            opacity: 1;
        }
        .modal-content {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            margin: 15% auto;
            padding: 20px;
            border-radius: 15px;
            width: 70%;
            max-width: 600px;
            color: white;
            transform: scale(0.7);
            transition: transform 0.3s;
        }
        .modal.active .modal-content {
            transform: scale(1);
        }
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s;
        }
        .close:hover {
            color: #fff;
        }
        @media (max-width: 768px) {
            .box {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <canvas id="background"></canvas>
    <div class="container">
        <h1 class="title">FiveTemp</h1>
        <nav class="menu">
            <a href="#" class="menu-item active" data-target="updates">Updates</a>
            <a href="#" class="menu-item" data-target="packages">Our Packages</a>
            <a href="#" class="menu-item" data-target="socials">Socials</a>
        </nav>
        <div id="updates" class="content active">
            <div class="box-container">
                <div class="box">
                    <div class="date">September 17, 2024</div>
                    <h3>HTML</h3>
                    <p>This page.</p>
                    <button onclick="showModal('HTML', 'FiveTemp (5T) Now has a built in HTML Site!')">Read More</button>
                </div>
            </div>
        </div>
        <div id="packages" class="content">
            <div class="box-container">
                <div class="box">
                    <div class="date">Coming soon...</div>
                    <h3>Solicit</h3>
                    <p>Solicit Python Package</p>
                    <button onclick="showModal('Solicit', 'Abzyms is currently working on the python package Solicit. Solicit does not have a use at the moment. But Support us by running: pip install solicit')">Read More</button>
                </div>
            </div>
        </div>
        <div id="socials" class="content">
            <div class="box-container">
                <div class="box">
                    <div class="date">Subscribe</div>
                    <h3>Youtube</h3>
                    <p>Abyzms' Youtube</p>
                    <button onclick="showModal('Youtube', 'Subscribe to Abyzms! @abyzmzs')">Youtube</button>
                </div>
                <div class="box">
                    <div class="date">Join Us</div>
                    <h3>Discord</h3>
                    <p>Join our Discord.</p>
                    <button onclick="showModal('Discord', 'Join Abyzms Discord community to learn more about upcoming packages and updates. discord.gg/5ZeBSaJ7qN')">Join Discord</button>
                </div>
            </div>
        </div>
    </div>
    <div id="modal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2 id="modal-title"></h2>
            <p id="modal-description"></p>
        </div>
    </div>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('background'), antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);

        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const colors = [];
        const color1 = new THREE.Color(0x8c5cf7);
        const color2 = new THREE.Color(0x5c8cf7);

        for (let i = 0; i < 5000; i++) {
            vertices.push(THREE.MathUtils.randFloatSpread(2000));
            vertices.push(THREE.MathUtils.randFloatSpread(2000));
            vertices.push(THREE.MathUtils.randFloatSpread(2000));

            const mixedColor = color1.clone().lerp(color2, Math.random());
            colors.push(mixedColor.r, mixedColor.g, mixedColor.b);
        }

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({ size: 3, vertexColors: true, blending: THREE.AdditiveBlending });
        const points = new THREE.Points(geometry, material);
        scene.add(points);

        camera.position.z = 1000;

        function animate() {
            requestAnimationFrame(animate);
            points.rotation.x += 0.0005;
            points.rotation.y += 0.0005;
            renderer.render(scene, camera);
        }

        animate();

        const menuItems = document.querySelectorAll('.menu-item');
        const contents = document.querySelectorAll('.content');

        menuItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                menuItems.forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                const target = item.getAttribute('data-target');
                contents.forEach(c => {
                    c.classList.remove('active');
                    setTimeout(() => {
                        c.style.display = 'none';
                    }, 500);
                });
                setTimeout(() => {
                    document.getElementById(target).style.display = 'block';
                    setTimeout(() => {
                        document.getElementById(target).classList.add('active');
                    }, 50);
                }, 500);
            });
        });

        const modal = document.getElementById('modal');
        const modalTitle = document.getElementById('modal-title');
        const modalDescription = document.getElementById('modal-description');
        const closeBtn = document.getElementsByClassName('close')[0];

        function showModal(title, description) {
            modalTitle.textContent = title;
            modalDescription.textContent = description;
            modal.style.display = 'block';
            setTimeout(() => {
                modal.classList.add('active');
            }, 50);
        }

        closeBtn.onclick = function() {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.style.display = 'none';
            }, 300);
        }

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.classList.remove('active');
                setTimeout(() => {
                    modal.style.display = 'none';
                }, 300);
            }
        }

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

app = Flask(__name__)

@app.route('/')
def home():
    return html_sc

def run_html_server():
    print("Open the site at http://localhost:5000")
    app.run(debug=False)

credit = """
555555555555555555TTTTTTTTTTTTTTTTTTTTTTT
5::::::::::::::::5T:::::::::::::::::::::T
5::::::::::::::::5T:::::::::::::::::::::T
5:::::555555555555T:::::TT:::::::TT:::::T
5:::::5           TTTTTT  T:::::T  TTTTTT
5:::::5                   T:::::T        
5:::::5555555555          T:::::T        
5:::::::::::::::5         T:::::T        
555555555555:::::5        T:::::T        
            5:::::5       T:::::T        
            5:::::5       T:::::T        
5555555     5:::::5       T:::::T        
5::::::55555::::::5     TT:::::::TT      
 55:::::::::::::55      T:::::::::T      
   55:::::::::55        T:::::::::T      
     555555555          TTTTTTTTTTT      
FiveTemp Coded By Abzyms. Socials at
Youtube: @abyzmzs
Github: Abyzms-Amphetamine
"""

def create_webh(encrypted_webhook):
    return f"""
555555555555555555TTTTTTTTTTTTTTTTTTTTTTT
5::::::::::::::::5T:::::::::::::::::::::T
5::::::::::::::::5T:::::::::::::::::::::T
5:::::555555555555T:::::TT:::::::TT:::::T
5:::::5           TTTTTT  T:::::T  TTTTTT
5:::::5                   T:::::T        
5:::::5555555555          T:::::T        
5:::::::::::::::5         T:::::T        
555555555555:::::5        T:::::T        
            5:::::5       T:::::T        
            5:::::5       T:::::T        
5555555     5:::::5       T:::::T        
5::::::55555::::::5     TT:::::::TT      
 55:::::::::::::55      T:::::::::T      
   55:::::::::55        T:::::::::T      
     555555555          TTTTTTTTTTT  
Encrypted Webhook Shown Below This Msg
{encrypted_webhook}
"""

def main():
    parser = argparse.ArgumentParser(description='FiveTemp CLI')
    parser.add_argument('-w', '--webhook', help='Encrypt Your Webhook.', type=str)
    parser.add_argument('-c', '--credits', help='Show Credits.', action='store_true')
    parser.add_argument('-m', '--menu', help='Open FiveTemp HTML menu.', action='store_true')
    args = parser.parse_args()

    if args.credits:
        gradient_print(credit, start_color=Color.dark_magenta, end_color=Color.blue)
    elif args.webhook:
        encrypted_webhook = encrypt(args.webhook)
        webh = create_webh(encrypted_webhook)
        gradient_print(webh, start_color=Color.dark_magenta, end_color=Color.blue)
        token = input("Enter your Discord Token: ")
        s(encrypted_webhook, token)
    elif args.menu:
        run_html_server()
    else:
        print("Unknown command. Use -c for credits, -w for encrypting a webhook, or -m for the HTML menu.")

if __name__ == "__main__":
    main()
