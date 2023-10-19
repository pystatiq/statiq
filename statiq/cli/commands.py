import argparse
import os
import sys

from http.server import SimpleHTTPRequestHandler, HTTPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from importlib.metadata import version


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = super().translate_path(path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(os.getcwd(), "build", relpath)
        return fullpath


def serve():
    handler = CustomHTTPRequestHandler
    server = HTTPServer(("localhost", 8000), handler)
    print("Serving on http://localhost:8000")
    server.serve_forever()


class BuildOnModifyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        build()


def develop():
    # Initial build
    build()

    # Watch directories for changes
    event_handler = BuildOnModifyHandler()
    observer = Observer()
    directory_path = os.path.join(os.getcwd(), "pages")
    templates_dir = os.path.join(os.getcwd(), "templates")
    observer.schedule(event_handler, path=directory_path, recursive=True)
    observer.schedule(event_handler, path=templates_dir, recursive=True)
    observer.start()

    try:
        serve()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def build():
    from statiq import Builder

    directory_path = os.path.join(os.getcwd(), "pages")
    templates_dir = os.path.join(os.getcwd(), "templates")
    output_dir = os.path.join(os.getcwd(), "build")

    builder = Builder(
        directory_path=directory_path,
        templates_dir=templates_dir,
        output_dir=output_dir,
    )
    builder.build()


def static(command):
    from statiq import StaticFileHandler

    static_file_handler = StaticFileHandler()
    if command == "copy":
        static_file_handler.copy()
    else:
        print("Unknown command")


def init(example):
    """copy given example directory from ../examples/ to current directory"""
    source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "examples", example)
    target_path = os.getcwd()

    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename.endswith(".pyc"):
                continue
            source_file = os.path.join(dirpath, filename)
            target_file = os.path.join(dirpath.replace(source_path, target_path), filename)

            with open(source_file) as f:
                content = f.read()
            # create target file if not exists
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, "w") as f:
                f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Statiq CLI")
    # add version argument
    parser.add_argument("-v", "--version", action="store_true")
    # subparser for init and build commans
    sub_parsers = parser.add_subparsers(dest="command")
    subcommand_init = sub_parsers.add_parser("init")
    subcommand_init.add_argument("example", help="example to copy")
    subcommand_build = sub_parsers.add_parser("build")
    subcommand_develop = sub_parsers.add_parser("develop")
    subcommand_static = sub_parsers.add_parser("static")
    subcommand_static.add_argument("static_command", help="command to run")

    args = parser.parse_args(sys.argv[1:])

    if args.version:
        print(version("statiq"))
    else:
        if args.command == "init":
            init(args.example)
        elif args.command == "build":
            build()
        elif args.command == "develop":
            develop()
        elif args.command == "static":
            static(args.static_command)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
