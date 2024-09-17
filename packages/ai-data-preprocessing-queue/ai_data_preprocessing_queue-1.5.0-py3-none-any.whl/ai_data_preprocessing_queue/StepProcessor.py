import importlib
from typing import Any

# required import because of logic in init
from . import Steps  # noqa: F401


class StepProcessor:
    def __init__(self, name: str, step_data: str | None) -> None:
        self.name: str = name
        self.step_data: str | None = step_data

        package_name = f"{__package__}.Steps"
        module_name = f".{self.name}"
        self.module = importlib.import_module(module_name, package_name)

        assert self.module.step is not None

    def run(self, item: Any, item_state: dict[str, Any], global_state: dict[str, Any] | None = None) -> Any:
        return self.module.step(item, item_state, global_state, self.step_data or "")
