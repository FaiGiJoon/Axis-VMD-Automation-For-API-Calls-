## 2025-05-15 - [Requests Session Optimization]
**Learning:** Disabling `trust_env` in `requests.Session` can significantly reduce overhead per request by skipping environment variable lookups for proxy configurations. This is especially beneficial in high-frequency polling scenarios or when many small requests are made to local/known devices.
**Action:** Always set `session.trust_env = False` when environment-based proxy configuration is not needed.
