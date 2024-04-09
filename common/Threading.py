from typing import Any, Callable
from concurrent.futures import ThreadPoolExecutor
import threading


class ManagedThreader:
    def __init__(self, max_workers: int, **resources) -> None:
        """Initializes the threading manager with a specific number of workers and shared resources.

        Args:
            max_workers (int): The maximum number of threads to run concurrently.
            **resources: Arbitrary keyword arguments representing shared resources.
        """
        self.max_workers = max_workers
        self.lock = threading.Lock()  # Common lock for all threads
        self.resources = resources  # Shared resources
        self.tasks = []  # Tasks to run

    def add_task(self, worker: Callable[..., Any], *args, **kwargs) -> None:
        """Adds a task to the thread pool.

        Args:
            worker (Callable[..., Any]): The worker function to run in a thread.
            *args: Positional arguments to pass to the worker function.
            **kwargs: Keyword arguments to pass to the worker function.
        """
        self.tasks.append((worker, args, kwargs))

    def run_all(self) -> None:
        """Starts executing all added tasks with thread pooling and waits for completion."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for worker, args, kwargs in self.tasks:
                # Pass the shared resources and the lock as keyword arguments.
                fut = executor.submit(worker, *args, **{**self.resources, "lock": self.lock, **kwargs})
                futures.append(fut)

            # Wait for all futures to complete.
            for future in futures:
                future.result()
