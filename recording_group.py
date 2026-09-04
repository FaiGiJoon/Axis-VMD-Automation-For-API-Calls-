from axis_base import AxisDevice
from recording_manager import RecordingManager

def list_recording_groups(device: AxisDevice):
    """
    Lists recording groups configured on the device.
    Delegates to RecordingManager for consistency across the framework.
    """
    return device.recording.list_recording_groups()
