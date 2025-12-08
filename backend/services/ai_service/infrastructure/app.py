"""Infrastructure entrypoint for the AI service.

This module keeps the long-running worker loop contained within the
infrastructure layer so the top-level entrypoint remains a thin shim.
"""

from __future__ import annotations

import time


def run_worker() -> None:
    """Start the placeholder AI worker loop.

    Replace this function with model loading and inference wiring when the
    service is ready to serve requests or background jobs.
    """

    print("AI service started. (placeholder)")
    while True:
        time.sleep(10)


if __name__ == "__main__":
    run_worker()
