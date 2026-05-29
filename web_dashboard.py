from flask import Flask, render_template, request, Response, flash, jsonify, send_file, session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, IPAddress, NumberRange, AnyOf, Regexp, Optional
import io
import os
import logging
from axis_base import AxisDevice
from zipstream import set_zipstream_strength
from shock_detection import set_axis_shock_sensitivity
from siren_light import control_siren

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CameraForm(FlaskForm):
    ip = StringField('Camera IP Address', validators=[DataRequired(), IPAddress()])
    username = StringField('Username', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9._-]+$', message="Invalid username format")])
    password = PasswordField('Password', validators=[DataRequired()])
    brightness = IntegerField('Brightness (0-100)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    contrast = IntegerField('Contrast (0-100)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    zipstream = SelectField('Zipstream Strength', choices=[
        ('off', 'Off'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('extreme', 'Extreme')
    ], validators=[DataRequired(), AnyOf(['off', 'low', 'medium', 'high', 'extreme'])])
    shock_sensitivity = IntegerField('Shock Sensitivity (0-100)', validators=[Optional(), NumberRange(min=0, max=100)], default=50)
    siren_active = BooleanField('Siren Active')
    vmd_enabled = BooleanField('Motion Detection Enabled')

def get_device_from_session():
    """Retrieves the device instance using credentials stored in the secure session."""
    ip = session.get('cam_ip')
    user = session.get('cam_user')
    password = session.get('cam_pass')
    if all([ip, user, password]):
        return AxisDevice(ip, user, password)
    return None

def sanitize_for_bat(value):
    if not isinstance(value, str):
        value = str(value)
    if '"' in value:
        raise ValueError("Double quotes are not allowed in configuration values.")
    return value.replace('%', '%%')

def generate_bat_content(ip, user, password, brightness, contrast, zipstream, shock_sensitivity, siren_active):
    s_ip = sanitize_for_bat(ip)
    s_user = sanitize_for_bat(user)
    s_pass = sanitize_for_bat(password)
    s_brightness = sanitize_for_bat(brightness)
    s_contrast = sanitize_for_bat(contrast)
    s_zipstream = sanitize_for_bat(zipstream)
    s_shock = sanitize_for_bat(shock_sensitivity)
    s_siren = "on" if siren_active else "off"
    s_siren_action = "start" if siren_active else "stop"

    bat = f"""@echo off
set "IP={s_ip}"
set "USER={s_user}"
set "PASS={s_pass}"

echo Setting Brightness to {s_brightness}...
curl -s --digest -u "%USER%:%PASS%" "http://%IP%/axis-cgi/param.cgi?action=update&root.Image.I0.Appearance.Brightness={s_brightness}"

echo Setting Contrast to {s_contrast}...
curl -s --digest -u "%USER%:%PASS%" "http://%IP%/axis-cgi/param.cgi?action=update&root.Image.I0.Appearance.Contrast={s_contrast}"

echo Setting Zipstream to {s_zipstream}...
curl -s --digest -u "%USER%:%PASS%" "http://%IP%/axis-cgi/zipstream/setstrength.cgi?strength={s_zipstream}"

echo Setting Shock Sensitivity to {s_shock}...
curl -s --digest -u "%USER%:%PASS%" "http://%IP%/axis-cgi/shockdetection/setsensitivitylevel.cgi?schemaversion=1&level={s_shock}"

echo Setting Siren to {s_siren}...
curl -s --digest -u "%USER%:%PASS%" "http://%IP%/axis-cgi/siren_and_light.cgi?action={s_siren_action}&siren={s_siren}"

echo Done!
pause
"""
    return bat

@app.route('/')
def index():
    form = CameraForm()
    return render_template('index.html', form=form)

@app.route('/snapshot')
def snapshot():
    device = get_device_from_session()
    if not device:
        # Return a placeholder if not connected
        return "Not connected", 401

    try:
        img_bytes = device.image.get_snapshot(resolution="640x360")
        return send_file(io.BytesIO(img_bytes), mimetype='image/jpeg')
    except Exception as e:
        logger.error(f"Failed to fetch snapshot: {e}")
        return str(e), 500

@app.route('/apps', methods=['POST'])
def list_apps():
    ip = request.form.get('ip')
    user = request.form.get('username')
    password = request.form.get('password')
    try:
        # Update session credentials
        session['cam_ip'] = ip
        session['cam_user'] = user
        session['cam_pass'] = password

        device = AxisDevice(ip, user, password)
        apps = device.apps.list_apps()
        return jsonify(apps)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/control_app', methods=['POST'])
def control_app():
    app_id = request.form.get('app_id')
    action = request.form.get('action')
    device = get_device_from_session()
    if not device:
        return jsonify({"error": "No active session"}), 401
    try:
        success = device.apps.control_app(app_id, action)
        return jsonify({"success": success})
    except Exception as e:
        logger.exception("Failed to control app")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/apply', methods=['POST'])
def apply_settings():
    form = CameraForm()
    if form.validate_on_submit():
        try:
            device = AxisDevice(form.ip.data, form.username.data, form.password.data)
            # Update session
            session['cam_ip'] = form.ip.data
            session['cam_user'] = form.username.data
            session['cam_pass'] = form.password.data

            device.param.update_params({
                "root.Image.I0.Appearance.Brightness": str(form.brightness.data),
                "root.Image.I0.Appearance.Contrast": str(form.contrast.data)
            })

            set_zipstream_strength(device, form.zipstream.data)

            if form.shock_sensitivity.data is not None:
                set_axis_shock_sensitivity(device, form.shock_sensitivity.data)

            control_siren(device, action="start" if form.siren_active.data else "stop")

            config = device.vmd.get_config()
            if config and 'profiles' in config:
                for profile in config['profiles']:
                    profile['enabled'] = form.vmd_enabled.data
                device.vmd.set_config(config)

            return "Settings applied successfully!"
        except Exception as e:
            logger.exception("Failed to apply settings")
            return "An internal error has occurred.", 500

    errors = ", ".join([f"{field}: {', '.join(errs)}" for field, errs in form.errors.items()])
    return f"Validation Error: {errors}", 400

@app.route('/download_bat', methods=['POST'])
def download_bat():
    form = CameraForm()
    if form.validate_on_submit():
        try:
            bat_content = generate_bat_content(
                form.ip.data, form.username.data, form.password.data,
                form.brightness.data, form.contrast.data, form.zipstream.data,
                form.shock_sensitivity.data, form.siren_active.data
            )
            return Response(
                bat_content,
                mimetype="text/plain",
                headers={"Content-disposition": "attachment; filename=setup_camera.bat"}
            )
        except ValueError as e:
            return f"Validation Error: {str(e)}", 400

    errors = ", ".join([f"{field}: {', '.join(errs)}" for field, errs in form.errors.items()])
    return f"Validation Error: {errors}", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
