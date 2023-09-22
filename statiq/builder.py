import re
import importlib.util
import os
import sys
from jinja2 import Environment, FileSystemLoader
from statiq.filters import head_element


class Builder:
    def __init__(
        self, directory_path="pages", templates_dir="templates", output_dir="build"
    ):
        self.routes = []
        template_dirs = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
            templates_dir,
        ]
        self.env = Environment(loader=FileSystemLoader(template_dirs))
        self.env.filters["head_element"] = head_element
        self.output_dir = output_dir
        self.config = self._load_config()
        self._load_filters_from_config()
        self._load_globals_from_config()
        self.register_directory(directory_path)

    def _load_config(self):
        # load config.py from the root of the project
        config_path = os.path.join(os.getcwd(), "config.py")
        if not os.path.exists(config_path):
            return {}
        spec = importlib.util.spec_from_file_location("config", config_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["config"] = module
        spec.loader.exec_module(module)
        return module

    def _load_filters_from_config(self):
        if not self.config:
            return
        if not hasattr(self.config, "FILTERS"):
            return
        if not isinstance(self.config.FILTERS, dict):
            return
        for filter_name, filter_function in self.config.FILTERS.items():
            self.env.filters[filter_name] = filter_function

    def _load_globals_from_config(self):
        if not self.config:
            return
        if not hasattr(self.config, "GLOBALS"):
            return
        if not isinstance(self.config.GLOBALS, dict):
            return
        for global_name, global_value in self.config.GLOBALS.items():
            self.env.globals[global_name] = global_value

    def register_directory(self, directory_path):
        for dirpath, _, filenames in os.walk(directory_path):
            py_files = [
                f for f in filenames if f.endswith(".py") and f != "__init__.py"
            ]

            for filename in py_files:
                filepath = os.path.join(dirpath, filename)

                spec = importlib.util.spec_from_file_location("module.name", filepath)

                module = importlib.util.module_from_spec(spec)

                sys.modules["module.name"] = module
                spec.loader.exec_module(module)

                if not hasattr(module, "page"):
                    continue

                if not callable(module.page):
                    continue

                page = module.page()
                template = self.env.get_template(page.template_path)

                if not page.path_parameters:
                    self.routes.append(
                        {"page": page, "template": template, "params": {}}
                    )
                else:
                    for params in page.path_parameters:
                        self.routes.append(
                            {"page": page, "template": template, "params": params}
                        )

    def build(self):
        for route in self.routes:
            data = route["page"].get_data(**route["params"])
            head = route["page"].get_head(**route["params"])
            html = route["template"].render(
                **data, head=head, path_parameters=route["params"]
            )
            filepath = route["page"].get_url(**route["params"])

            print("Generating page:", filepath)
            filepath = os.path.join(self.output_dir, filepath)
            os.makedirs(
                os.path.dirname(filepath),
                exist_ok=True,
            )

            # write to file
            with open(filepath, "w") as f:
                f.write(html)
