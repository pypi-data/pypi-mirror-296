import re
from io import StringIO
from typing import Any

import pandas


def step(item: Any, item_state: dict[str, Any], global_state: dict[str, Any] | None, preprocessor_data: str) -> Any:
    if preprocessor_data is None or not preprocessor_data:
        return item

    csv = _get_data_from_store_or_reload(global_state, preprocessor_data)

    for _, row in csv.iterrows():
        pattern = re.compile(row[0])
        item = pattern.sub(" " + row[1] + " ", item)

    return item


def _get_data_from_store_or_reload(global_state: dict[str, Any] | None, preprocessor_data: str) -> pandas.DataFrame:
    if global_state is None:
        return _prepare_pre_processor_data(preprocessor_data)

    dict_identifier = "regexReplacementpreprocessor_data"
    if dict_identifier in global_state:
        return global_state[dict_identifier]

    prepared_data = _prepare_pre_processor_data(preprocessor_data)
    global_state[dict_identifier] = prepared_data
    return prepared_data


def _prepare_pre_processor_data(preprocessor_data: str) -> pandas.DataFrame:
    csv = pandas.read_csv(StringIO(preprocessor_data), header=None, usecols=[0, 1, 2], quotechar='"', encoding="utf8")

    csv[0] = csv[0].str.strip()
    csv[1] = csv[1].str.strip()
    csv[2] = pandas.to_numeric(csv[2])
    csv["sort"] = csv[2]

    # sort
    return csv.sort_values("sort", inplace=False).drop("sort", axis=1)
