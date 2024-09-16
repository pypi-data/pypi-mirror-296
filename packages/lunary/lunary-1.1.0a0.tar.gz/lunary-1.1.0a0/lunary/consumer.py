import time
from typing import Any, cast
import atexit
import requests
import logging
from threading import Thread
import jsonpickle
from .config import get_config

logger = logging.getLogger(__name__)

MAX_BATCH_SIZE = 4.9 * 1024 * 1024  # 4.9MB in bytes


class Consumer(Thread):

    def __init__(self, event_queue, app_id=None):
        self.running = True
        self.event_queue = event_queue
        self.app_id = app_id

        Thread.__init__(self, daemon=True)
        atexit.register(self.stop)

    def run(self):
        while self.running:
            self.send_batch()
            time.sleep(0.5)

        self.send_batch()

    def send_batch(self):
        config = get_config()
        batch = self.event_queue.get_batch()

        verbose = config.verbose
        api_url = config.api_url

        if len(batch) == 0:
            return

        token = batch[0].get("appId") or self.app_id or config.app_id

        sub_batches = self.split_into_sub_batches(batch)

        for sub_batch in sub_batches:
            if verbose:
                logging.info(f"Sending {len(sub_batch)} events.")

            try:
                if verbose:
                    logging.info(f"Sending events to {api_url}")

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }

                data = jsonpickle.encode({"events": sub_batch}, unpicklable=False)
                response = requests.post(
                    api_url + "/v1/runs/ingest",
                    data=data,
                    headers=headers,
                    verify=config.ssl_verify,
                )
                response.raise_for_status()

                if verbose:
                    logging.info(f"Events sent. Status code: {response.status_code}")
            except Exception as e:
                if verbose:
                    logging.exception(f"Error sending events: {e}")
                else:
                    logging.error("Error sending events")

                self.event_queue.append(sub_batch)

    def split_into_sub_batches(self, batch: list[dict[str, Any]]):
        sub_batches = []
        current_batch = []
        current_size = 0

        for event in batch:
            event_data = cast(str, jsonpickle.encode(event, unpicklable=False))
            event_size = len(event_data.encode("utf-8"))

            if event_size > MAX_BATCH_SIZE:
                logging.error(
                    "[LUNARY] An individual event exceeds the maximum batch size of 5MB and will be skipped."
                )
                continue  # Skip events that are too large

            if current_size + event_size > MAX_BATCH_SIZE:
                if current_batch:
                    sub_batches.append(current_batch)
                current_batch = [event]
                current_size = event_size
            else:
                current_batch.append(event)
                current_size += event_size

        if current_batch:
            sub_batches.append(current_batch)

        return sub_batches

    def stop(self):
        self.running = False
        self.join()
