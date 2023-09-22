import argparse
import os
import sys


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


def init(example):
    """copy given example directory from ../examples/ to current directory"""
    source_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "examples", example
    )
    target_path = os.getcwd()

    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename.endswith(".pyc"):
                continue
            source_file = os.path.join(dirpath, filename)
            target_file = os.path.join(
                dirpath.replace(source_path, target_path), filename
            )

            with open(source_file) as f:
                content = f.read()
            # create target file if not exists
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            with open(target_file, "w") as f:
                f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Statiq CLI")
    # add version argument
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.0.2")
    # subparser for init and build commans
    sub_parsers = parser.add_subparsers(dest="command")
    subcommand_init = sub_parsers.add_parser("init")
    subcommand_init.add_argument("example", help="example to copy")

    subcommand_build = sub_parsers.add_parser("build")

    args = parser.parse_args(sys.argv[1:])

    if args.command == "init":
        init(args.example)
    elif args.command == "build":
        build()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
