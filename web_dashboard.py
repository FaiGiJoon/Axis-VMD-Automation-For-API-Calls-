from flask import Flask, render_template, request, send_file
import io
from axis_base import AxisDevice
from param_manager import ParamManager
from zipstream import set_zipstream_strength

app = Flask(__name__)

def generate_bat_content(ip, user, password, brightness, contrast, zipstream):
    bat = f"""@echo off
set IP={ip}
set USER={user}
set PASS={password}

echo Setting Brightness to {brightness}...
curl -s --digest -u %USER%:%PASS% "http://%IP%/axis-cgi/param.cgi?action=update&root.Image.I0.Appearance.Brightness={brightness}"

echo Setting Contrast to {contrast}...
curl -s --digest -u %USER%:%PASS% "http://%IP%/axis-cgi/param.cgi?action=update&root.Image.I0.Appearance.Contrast={contrast}"

echo Setting Zipstream to {zipstream}...
curl -s --digest -u %USER%:%PASS% "http://%IP%/axis-cgi/zipstream/setstrength.cgi?strength={zipstream}"

echo Done!
pause
"""
    return bat

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['POST'])
def apply_settings():
    ip = request.form.get('ip')
    user = request.form.get('username')
    password = request.form.get('password')
    brightness = request.form.get('brightness')
    contrast = request.form.get('contrast')
    zipstream = request.form.get('zipstream')

    try:
        # Use trust_env=False for performance as per guidelines
        device = AxisDevice(ip, user, password, trust_env=False)
        pm = ParamManager(device)

        # Batch updates for performance
        pm.update_params({
            "root.Image.I0.Appearance.Brightness": brightness,
            "root.Image.I0.Appearance.Contrast": contrast
        })

        # Zipstream strength
        set_zipstream_strength(device, zipstream)

        return "Settings applied successfully!"
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/download_bat', methods=['POST'])
def download_bat():
    ip = request.form.get('ip')
    user = request.form.get('username')
    password = request.form.get('password')
    brightness = request.form.get('brightness')
    contrast = request.form.get('contrast')
    zipstream = request.form.get('zipstream')

    bat_content = generate_bat_content(ip, user, password, brightness, contrast, zipstream)

    buffer = io.BytesIO()
    buffer.write(bat_content.encode('utf-8'))
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="setup_camera.bat",
        mimetype="text/plain"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
