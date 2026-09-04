import requests
from requests.auth import HTTPDigestAuth
import logging

logger = logging.getLogger(__name__)

class AxisDevice:
    def __init__(self, ip, user, password, trust_env=False, timeout=10):
        self.ip = ip
        self.url_base = f"http://{ip}"
        self.session = requests.Session()
        self.session.trust_env = trust_env
        self.session.auth = HTTPDigestAuth(user, password)
        self.timeout = timeout

        # Cache for lazy-loaded managers
        self._param = None
        self._vmd = None
        self._ptz = None
        self._mqtt = None
        self._overlay = None
        self._storage = None
        self._apps = None
        self._aoa = None
        self._image = None
        self._recording = None
        self._device_data_hub = None

    def get(self, path, params=None, stream=False):
        try:
            response = self.session.get(f"{self.url_base}{path}", params=params, timeout=self.timeout, stream=stream)
            if not stream:
                if response.encoding is None:
                    response.encoding = 'utf-8'
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request failed: {e}")
            raise

    def post(self, path, json_data=None, params=None):
        try:
            response = self.session.post(f"{self.url_base}{path}", json=json_data, params=params, timeout=self.timeout)
            if response.encoding is None:
                response.encoding = 'utf-8'
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request failed: {e}")
            raise

    @property
    def param(self):
        if self._param is None:
            from param_manager import ParamManager
            self._param = ParamManager(self)
        return self._param

    @property
    def vmd(self):
        if self._vmd is None:
            from vmd_manager import VMDManager
            self._vmd = VMDManager(self)
        return self._vmd

    @property
    def ptz(self):
        if self._ptz is None:
            from ptz_manager import PTZManager
            self._ptz = PTZManager(self)
        return self._ptz

    @property
    def mqtt(self):
        if self._mqtt is None:
            from mqtt_manager import MQTTManager
            self._mqtt = MQTTManager(self)
        return self._mqtt

    @property
    def overlay(self):
        if self._overlay is None:
            from overlay_manager import OverlayManager
            self._overlay = OverlayManager(self)
        return self._overlay

    @property
    def storage(self):
        if self._storage is None:
            from storage_manager import StorageManager
            self._storage = StorageManager(self)
        return self._storage

    @property
    def apps(self):
        if self._apps is None:
            from app_manager import AppManager
            self._apps = AppManager(self)
        return self._apps

    @property
    def aoa(self):
        if self._aoa is None:
            from object_analytics_manager import ObjectAnalyticsManager
            self._aoa = ObjectAnalyticsManager(self)
        return self._aoa

    @property
    def image(self):
        if self._image is None:
            from image_manager import ImageManager
            self._image = ImageManager(self)
        return self._image

    @property
    def recording(self):
        if self._recording is None:
            from recording_manager import RecordingManager
            self._recording = RecordingManager(self)
        return self._recording

    @property
    def device_data_hub(self):
        if self._device_data_hub is None:
            from device_data_hub_manager import DeviceDataHubManager
            self._device_data_hub = DeviceDataHubManager(self)
        return self._device_data_hub
