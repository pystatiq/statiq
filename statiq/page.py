import os
import inspect
import re
from typing import Union, Callable, List, Dict, Any
from types import FrameType, ModuleType


class Page:
    def __init__(
        self,
        data: Union[Callable, List] = None,
        head: Union[Callable, List[Union[Dict, str]]] = [],
        path_parameters: Union[Callable, List[Dict]] = [],
        template_path: str = "",
    ):
        self.head = head
        self.path_parameters = (
            path_parameters() if callable(path_parameters) else path_parameters
        )
        frame = inspect.currentframe().f_back  # Get the frame of the caller
        module = inspect.getmodule(frame)  # Get the module of the caller
        module_path = (
            f"{module.__file__ if hasattr(module, '__file__') else module.__name__}"
        )

        template_path = module_path.replace(".py", ".html").split("pages/")[1]
        self.template_path = template_path

        self._validate_params(self.path_parameters)

        self.data = data

    def _get_caller_frame(self) -> Union[FrameType, None]:
        return inspect.currentframe().f_back

    def _get_module(self) -> Union[ModuleType, None]:
        frame = self._get_caller_frame()
        return inspect.getmodule(frame)

    def _get_module_path(self) -> str:
        module = self._get_module()
        return module.__file__ if hasattr(module, "__file__") else module.__name__

    def _set_template_path(self, template_path: str) -> None:
        self.template_path = template_path

    def _get_path_params(self) -> List[str]:
        return re.findall(r"\[([\w\d]+)\]", self.template_path)

    def get_data(self, **parameters) -> Any:
        return self.data(**parameters) if callable(self.data) else self.data

    def get_head(self, **parameters) -> Any:
        return self.head(**parameters) if callable(self.head) else self.head

    def _render_template(self, **parameters) -> str:
        template = self.env.get_template(self.template_path)
        return template.render(**parameters, head=self.head)

    def get_url(self, **parameters) -> str:
        url = self.template_path
        for param in self.path_params:
            url = url.replace(f"[{param}]", parameters[param])
        return url

    def _get_module_path(self):
        frame = inspect.currentframe().f_back  # Get the frame of the caller
        module = inspect.getmodule(frame)  # Get the module of the caller

    @property
    def default_template_path(self):
        return self._get_default_template_path()

    @property
    def path_params(self):
        return self._get_path_params()

    def _validate_params(self, params) -> None:
        for param_dict in params:
            for param in self.path_params:
                if param not in param_dict:
                    raise Exception(f"Path parameter '{param}' not in params list")
