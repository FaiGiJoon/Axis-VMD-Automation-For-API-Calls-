import io

class ImageManager:
    def __init__(self, device):
        self.device = device

    def get_snapshot(self, resolution=None, camera=1):
        """
        Retrieves a JPEG snapshot from the camera.
        :param resolution: String like '1280x720'.
        :param camera: Camera/source index.
        """
        path = "/axis-cgi/jpg/image.cgi"
        params = {"camera": camera}
        if resolution:
            params["resolution"] = resolution

        response = self.device.get(path, params=params, stream=True)
        return response.content

    def get_cv2_frame(self, resolution=None, camera=1):
        """
        Retrieves a snapshot and decodes it into an OpenCV-compatible NumPy array.
        Requires numpy and opencv-python to be installed.
        """
        try:
            import cv2
            import numpy as np
        except ImportError:
            raise ImportError("OpenCV and NumPy are required for get_cv2_frame().")

        img_bytes = self.get_snapshot(resolution, camera)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return frame

    def save_snapshot(self, filepath, resolution=None, camera=1):
        """Saves a snapshot to a file."""
        img_bytes = self.get_snapshot(resolution, camera)
        with open(filepath, 'wb') as f:
            f.write(img_bytes)
        return filepath
