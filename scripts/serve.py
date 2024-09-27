from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer
from threading import Thread
import time
from watchdog.observers import Observer
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEventHandler

from . import build

class BuildEventHanlder(FileSystemEventHandler):
    """Build Event Handler."""

    def on_modified(self, event):
        """On file modification."""
        src_path = Path(event.src_path).relative_to(Path.cwd())
        print(f"File changed: {src_path}, rebuilding...")
        build.build_file(src_path)

    def on_created(self, event):
        """On file creation."""
        src_path = Path(event.src_path).relative_to(Path.cwd())
        print(f"File created: {src_path}, rebuilding...")
        build.build_file(src_path)

def start_http_server(directory: Path, port: int = 8000):
    """Start a simple HTTP server."""

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    with TCPServer(("", port), Handler) as httpd:
        print(f"Serving HTTP on port {port} from {directory}")
        httpd.serve_forever()


def serve():
    """Build."""
    build.build()

    http_server = Thread(target=start_http_server, args=(build.DST_PATH,))
    http_server.daemon = True
    http_server.start()

    event_handler = BuildEventHanlder()
    observer = Observer()
    observer.schedule(event_handler, build.SRC_PATH, recursive=True)
    observer.setDaemon(True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except:
        observer.stop()

    observer.join()
    http_server.join()


if __name__ == "__main__":
    serve()
