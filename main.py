import time
import threading
import random

from common.Threading import ManagedThreader


class MyClass:
    def __init__(self, text):
        self.text = text


def worker(task_id: int, lock: threading.Lock, my_class: MyClass) -> None:
    with lock:
        my_class.text += "."
        print(my_class.text)

    with lock:
        print(f"#{task_id:03} - Started")

    time.sleep(random.randint(1, 10))

    with lock:
        print(f"#{task_id:03} - Ended")


my_class = MyClass("|")

managed_threader = ManagedThreader(max_workers=2, my_class=my_class)

for i in range(5):
    managed_threader.add_task(worker, i)

managed_threader.run_all()

