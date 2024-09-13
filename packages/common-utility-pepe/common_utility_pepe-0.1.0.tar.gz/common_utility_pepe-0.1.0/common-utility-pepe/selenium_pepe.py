
from collections import deque
import time

class SeleniumPepe:
    def __init__(self, max_request_count=200, time_limit=60):
        self.max_request_count = max_request_count
        self.time_limit = time_limit
        self.timestamps = deque(maxlen=max_request_count)

    def rate_limited_execute_script(self, driver, script):
        current_time = time.time()
        if len(self.timestamps) == self.max_request_count:
            oldest_request_time = self.timestamps[0]
            time_since_oldest = current_time - oldest_request_time
            if time_since_oldest < self.time_limit:
                time.sleep(self.time_limit - time_since_oldest)

        driver.execute_script(script)
        self.timestamps.append(time.time())
        return driver
