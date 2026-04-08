def set_axis_shock_sensitivity(device, level):
    """
    Sets the shock detection sensitivity on an Axis camera.
    
    :param device: The authenticated session object (e.g., requests.Session() or custom Axis object)
    :param level: Integer between 0 (lowest) and 100 (highest)
    :return: The XML response text from the camera
    """
    # 1. Validate the input range to prevent API errors
    if not (0 <= level <= 100):
        raise ValueError("Sensitivity level must be between 0 and 100.")

    # 2. Define the exact CGI path and required parameters
    path = "/axis-cgi/shockdetection/setsensitivitylevel.cgi"
    params = {
        "schemaversion": "1",  # Required for this API
        "level": str(level)
    }

    # 3. Execute the GET request
    # Ensure your 'device' object handles Digest or Basic authentication
    try:
        response = device.get(path, params=params)
        response.raise_for_status()  # Check for 401, 404, or 500 errors
        return response.text
    except Exception as e:
        return f"Failed to set sensitivity: {str(e)}"

# Example Usage:
# result = set_axis_shock_sensitivity(my_camera, 75)
# print(result)
