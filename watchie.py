import time
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WatchieEventHandler(FileSystemEventHandler):
    def __init__(self, result_fn, path=None):
        super().__init__()
        self.result_fn = result_fn
        self.path = path

    def on_created(self, event):
        if self.path:
            if os.path.abspath(self.path) == event.src_path:
                print("Reloading {}".format(event.src_path))
                self.result_fn()

    def on_modified(self, event):
        if not self.path:
            print("Reloading {}".format(event.src_path))
            self.result_fn()

class Watchie():

    def __init__(self):
        self.observer = Observer()

    def watch(self, result_fn, path='.', recursive=True):
        if os.path.isdir(path):
            event_handler = WatchieEventHandler(result_fn)
            self.observer.schedule(event_handler, path, recursive=recursive)
        else:
            dirname = os.path.dirname(os.path.abspath(path))
            event_handler = WatchieEventHandler(result_fn, path)
            self.observer.schedule(event_handler, dirname, recursive=False)

    def start(self):
        print("Night gathers, and now my watch begins...")
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


if __name__=='__main__':
    w = Watchie()
    w.watch(path="watchie.py",
            result_fn=lambda: print("Who watches the watchie?"))
    w.watch(path=".",
            result_fn=lambda: print("Directory-level change!"))
    w.start()
