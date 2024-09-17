from typing import Any

from .StepProcessor import StepProcessor


class Pipeline:
    def __init__(self, step_dict: dict[str, str | None]) -> None:
        self.step_processors: list[StepProcessor] = []
        for step_name in list(filter(None, step_dict.keys())):
            processor = StepProcessor(step_name, step_dict.get(step_name))
            self.step_processors.append(processor)

    def consume(self, item: Any, global_state: dict[str, Any] | None = None) -> Any:
        ret_val = item

        item_state: dict[str, Any] = {}
        for processor in self.step_processors:
            ret_val = processor.run(ret_val, item_state, global_state)

        return ret_val
