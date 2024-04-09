import os
import sys
import pytest
import threading
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.Threading import ManagedThreader


# A simple worker function for testing
def worker(task_id: int, lock: threading.Lock, sleep_time: int = 1, **kwargs) -> str:
    time.sleep(sleep_time)

    return f"Task {task_id} completed"


def test_managed_threader_with_single_worker():
    """Test ManagedThreader with a single worker."""
    threader = ManagedThreader(max_workers=1)
    threader.add_task(worker, 1, sleep_time=1)
    threader.run_all()
    # Success if no exceptions are raised


def test_managed_threader_with_multiple_workers():
    """Test ManagedThreader runs tasks concurrently with multiple workers."""
    threader = ManagedThreader(max_workers=4)
    threader.add_task(worker, 1, sleep_time=1)
    threader.add_task(worker, 2, sleep_time=1)
    threader.add_task(worker, 3, sleep_time=1)
    threader.add_task(worker, 4, sleep_time=1)

    start_time = time.time()
    threader.run_all()
    end_time = time.time()

    # Verify tasks were run concurrently

    assert end_time - start_time < 2, "Tasks did not run concurrently"


def test_managed_threader_shared_resource():
    """Test that ManagedThreader passes shared resources to worker functions."""
    shared_data = {"test_data": "shared value"}

    def resource_worker(task_id: int, lock: threading.Lock, test_data: str = "") -> str:
        with lock:
            return test_data

    threader = ManagedThreader(max_workers=1, test_data=shared_data["test_data"])
    threader.add_task(resource_worker, 1)
    threader.run_all()
    # Success if no exceptions are raised and shared resource is correctly passed


if __name__ == "__main__":
    pytest.main()
