from flask import Flask, Response, render_template
from io import BytesIO
from PIL import ImageGrab
import logging
import os
import sys
import ifaddr
import re

base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

app = Flask(__name__,
            static_folder=os.path.join(base_dir, 'static'),
            template_folder=os.path.join(base_dir, 'templates'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    while True:
        img_buffer = BytesIO()
        ImageGrab.grab().save(img_buffer, 'JPEG', quality=50)
        img_buffer.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + img_buffer.read() + b'\r\n\r\n')


if __name__ == '__main__':
    def get_v4(ip, adapter):
        if re.match(r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$", ip):
            print(f'• Sharing screen on ip => http://{ip}:6999 \tof "{adapter}"')


    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    cli = lambda *x: None
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    APP_TITLE = """
               

 .----------------. .----------------. .----------------. .----------------. .----------------. .-----------------.
| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |
| |    _______   | | |     ______   | | |  _______     | | |  _________   | | |  _________   | | | ____  _____  | |
| |   /  ___  |  | | |   .' ___  |  | | | |_   __ \    | | | |_   ___  |  | | | |_   ___  |  | | ||_   \|_   _| | |
| |  |  (__ \_|  | | |  / .'   \_|  | | |   | |__) |   | | |   | |_  \_|  | | |   | |_  \_|  | | |  |   \ | |   | |
| |   '.___`-.   | | |  | |         | | |   |  __ /    | | |   |  _|  _   | | |   |  _|  _   | | |  | |\ \| |   | |
| |  |`\____) |  | | |  \ `.___.'\  | | |  _| |  \ \_  | | |  _| |___/ |  | | |  _| |___/ |  | | | _| |_\   |_  | |
| |  |_______.'  | | |   `._____.'  | | | |____| |___| | | | |_________|  | | | |_________|  | | ||_____|\____| | |
| |              | | |              | | |              | | |              | | |              | | |              | |
| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |
 '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' 
 .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. 
| .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |
| |     ______   | | |      __      | | |    _______   | | |  _________   | | |  _________   | | |  _______     | |
| |   .' ___  |  | | |     /  \     | | |   /  ___  |  | | | |  _   _  |  | | | |_   ___  |  | | | |_   __ \    | |
| |  / .'   \_|  | | |    / /\ \    | | |  |  (__ \_|  | | | |_/ | | \_|  | | |   | |_  \_|  | | |   | |__) |   | |
| |  | |         | | |   / ____ \   | | |   '.___`-.   | | |     | |      | | |   |  _|  _   | | |   |  __ /    | |
| |  \ `.___.'\  | | | _/ /    \ \_ | | |  |`\____) |  | | |    _| |_     | | |  _| |___/ |  | | |  _| |  \ \_  | |
| |   `._____.'  | | ||____|  |____|| | |  |_______.'  | | |   |_____|    | | | |_________|  | | | |____| |___| | |
| |              | | |              | | |              | | |              | | |              | | |              | |
| '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |
 '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' 
                                                                                
                                                        
                    
                                                                                                 
                """
    print(APP_TITLE)
    network_adapters = ifaddr.get_adapters()

    for adapter in network_adapters:
        for ip in adapter.ips:
            get_v4(str(ip.ip), str(adapter.nice_name))
    print('\n** (Press CTRL+C) to stop screen share')
    app.run(host='0.0.0.0', port=6999, debug=False)
