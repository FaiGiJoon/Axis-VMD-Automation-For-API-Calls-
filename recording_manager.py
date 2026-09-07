from axis_base import AxisDevice

class RecordingManager:
    """Manager for Axis Recording APIs (Recording Search, Notify, Playback, and Group)."""
    def __init__(self, device: AxisDevice):
        self.device = device

    def list_recording_groups(self):
        """Lists recording groups configured on the device."""
        path = "/axis-cgi/record/recording_group/list.cgi"
        return self.device.get(path, params={"schemaversion": "1"}).text

    def search_recordings(self, start_time=None, stop_time=None, recording_id=None):
        """
        Searches recorded video/audio clips on edge/network storage.
        :param start_time: Optional start timestamp (ISO 8601 string)
        :param stop_time: Optional stop timestamp (ISO 8601 string)
        :param recording_id: Optional specific recording ID
        """
        path = "/axis-cgi/record/search.cgi"
        params = {"schemaversion": "1"}
        if start_time:
            params["starttime"] = start_time
        if stop_time:
            params["stoptime"] = stop_time
        if recording_id:
            params["recordingid"] = recording_id
        return self.device.get(path, params=params).text

    def get_playback_uri(self, recording_id, stream_format="h264"):
        """
        Retrieves playback stream URI for a given recording ID.
        :param recording_id: Recording identifier
        :param stream_format: Stream video format (e.g., h264, h265)
        """
        path = "/axis-cgi/record/playback.cgi"
        params = {
            "schemaversion": "1",
            "recordingid": recording_id,
            "format": stream_format
        }
        return self.device.get(path, params=params).text

    def get_recording_status(self):
        """Retrieves status of active recordings and recording devices."""
        path = "/axis-cgi/record/status.cgi"
        return self.device.get(path, params={"schemaversion": "1"}).text

    def get_recording_spans(self, recording_id=None):
        """Retrieves recording spans for recordings (Recording Search API)."""
        path = "/axis-cgi/record/spans.cgi"
        params = {"schemaversion": "1"}
        if recording_id:
            params["recordingid"] = recording_id
        return self.device.get(path, params=params).text

    def get_recording_segments(self, recording_id=None, span_id=None):
        """Retrieves recording segments for a span (Recording Playback API)."""
        path = "/axis-cgi/record/segments.cgi"
        params = {"schemaversion": "1"}
        if recording_id:
            params["recordingid"] = recording_id
        if span_id:
            params["spanid"] = span_id
        return self.device.get(path, params=params).text
