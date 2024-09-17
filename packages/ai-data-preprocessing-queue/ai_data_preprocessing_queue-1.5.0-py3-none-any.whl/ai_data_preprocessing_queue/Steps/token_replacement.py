import re
from typing import Any


# the higher the number the higher the prio
def step(item: Any, item_state: dict[str, Any], global_state: dict[str, Any] | None, preprocessor_data: str) -> Any:
    if preprocessor_data is None or not preprocessor_data:
        return item

    lines = _get_data_from_store_or_reload(global_state, preprocessor_data)

    for line in lines:
        escaped = re.escape(line[0])
        regex = "\\b" + escaped

        # also replace dots at end of word
        if not line[0].endswith("."):
            regex = regex + "\\b"

        pattern = re.compile(regex)
        item = pattern.sub(line[1], item)

    return item


def _get_data_from_store_or_reload(global_state: dict[str, Any] | None, preprocessor_data: str) -> list[list[str]]:
    if global_state is None:
        return _prepare_pre_processor_data(preprocessor_data)

    dict_identifier = "tokenReplacementpreprocessor_data"
    if dict_identifier in global_state:
        return global_state[dict_identifier]

    prepared_data = _prepare_pre_processor_data(preprocessor_data)
    global_state[dict_identifier] = prepared_data
    return prepared_data


def _prepare_pre_processor_data(preprocessor_data: str) -> list[list[str]]:
    lines: list[list[str]] = [
        [s.strip() for i, s in enumerate(line.split(",")) if (i == 2 and re.compile(r"^[0-9\s]+$").match(s)) or i < 2]
        for line in preprocessor_data.splitlines()
        if line.count(",") == 2
    ]
    lines = [line for line in lines if len(line) == 3]

    i: int = 0
    while i < len(lines):
        lines[i][2] = int(lines[i][2])  # type: ignore
        i += 1

    # sort
    lines = sorted(lines, key=lambda f: 0 - f[2])  # type: ignore

    return lines
