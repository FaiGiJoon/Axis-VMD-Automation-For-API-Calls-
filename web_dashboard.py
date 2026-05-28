from flask import Flask, render_template, request, Response, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, IPAddress, NumberRange, AnyOf, Regexp, Optional
import io
import os
import logging
from axis_base import AxisDevice
from param_manager import ParamManager
from zipstream import set_zipstream_strength
from shock_detection import set_axis_shock_sensitivity
from siren_light import control_siren
from vmd_manager import VMDManager

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

def sanitize_for_bat(value):
    """
    Sanitizes values for use in a Windows batch file.
    Since we use 'set "VAR=VAL"', we must forbid double quotes.
    Other special characters are safe inside the quoted assignment
    for the 'set' command itself, but we should be careful when they
    are expanded later.
    """
    if not isinstance(value, str):
        value = str(value)
    # Double quotes are dangerous in batch scripts and hard to escape safely
    # in this context. We forbid them to prevent injection.
    if '"' in value:
        raise ValueError("Double quotes are not allowed in configuration values.")
    # In .bat files, % must be escaped as %% to be treated literally
    return value.replace('%', '%%')

def generate_bat_content(ip, user, password, brightness, contrast, zipstream, shock_sensitivity, siren_active):
    # Sanitize inputs
    s_ip = sanitize_for_bat(ip)
    s_user = sanitize_for_bat(user)
    s_pass = sanitize_for_bat(password)
    s_brightness = sanitize_for_bat(brightness)
    s_contrast = sanitize_for_bat(contrast)
    s_zipstream = sanitize_for_bat(zipstream)
    s_shock = sanitize_for_bat(shock_sensitivity)
    s_siren = "on" if siren_active else "off"
    s_siren_action = "start" if siren_active else "stop"

    # Use the 'set "VAR=VAL"' syntax which is robust in Windows batch
    # for most special characters except double quotes.
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

rem NOTE: VMD (Motion Detection) configuration is complex and requires JSON payload.
rem Please use the web dashboard to enable/disable VMD.

echo Done!
pause
"""
    return bat

@app.route('/')
def index():
    form = CameraForm()
    return render_template('index.html', form=form)

@app.route('/apply', methods=['POST'])
def apply_settings():
    form = CameraForm()
    if form.validate_on_submit():
        ip = form.ip.data
        user = form.username.data
        password = form.password.data
        brightness = form.brightness.data
        contrast = form.contrast.data
        zipstream = form.zipstream.data
        shock_sensitivity = form.shock_sensitivity.data
        siren_active = form.siren_active.data
        vmd_enabled = form.vmd_enabled.data

        try:
            device = AxisDevice(ip, user, password, trust_env=False)
            pm = ParamManager(device)

            # Update Image Parameters
            pm.update_params({
                "root.Image.I0.Appearance.Brightness": str(brightness),
                "root.Image.I0.Appearance.Contrast": str(contrast)
            })

            # Update Zipstream
            set_zipstream_strength(device, zipstream)

            # Update Shock Sensitivity
            if shock_sensitivity is not None:
                set_axis_shock_sensitivity(device, shock_sensitivity)

            # Update Siren
            control_siren(device, action="start" if siren_active else "stop")

            # Update VMD
            vmd = VMDManager(device)
            config = vmd.get_config()
            if config and 'profiles' in config:
                for profile in config['profiles']:
                    profile['enabled'] = vmd_enabled
                vmd.set_config(config)

            return "Settings applied successfully!"
        except Exception as e:
            logger.error(f"Failed to apply settings to {ip}: {str(e)}")
            return "Error: Failed to apply settings to the camera.", 500

    errors = ", ".join([f"{field}: {', '.join(errs)}" for field, errs in form.errors.items()])
    return f"Validation Error: {errors}", 400

@app.route('/download_bat', methods=['POST'])
def download_bat():
    form = CameraForm()
    if form.validate_on_submit():
        ip = form.ip.data
        user = form.username.data
        password = form.password.data
        brightness = form.brightness.data
        contrast = form.contrast.data
        zipstream = form.zipstream.data
        shock_sensitivity = form.shock_sensitivity.data
        siren_active = form.siren_active.data

        try:
            bat_content = generate_bat_content(ip, user, password, brightness, contrast, zipstream, shock_sensitivity, siren_active)
            return Response(
                bat_content,
                mimetype="text/plain",
                headers={"Content-disposition": "attachment; filename=setup_camera.bat"}
            )
        except ValueError as e:
            logger.warning(f"Validation error while generating BAT for {ip}: {str(e)}")
            return "Validation Error: Invalid input provided.", 400
           

    errors = ", ".join([f"{field}: {', '.join(errs)}" for field, errs in form.errors.items()])
    return f"Validation Error: {errors}", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
