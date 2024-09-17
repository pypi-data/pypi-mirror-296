from functools import reduce
from typing import Any, cast

import numpy as np


def step(item: Any, item_state: dict[str, Any], global_state: dict[str, Any] | None, preprocessor_data: str) -> Any:
    if preprocessor_data is None:
        return item

    words = preprocessor_data.splitlines()

    if not words:
        return item

    values = {len(w) for w in words}
    grouped_replace_words = [{"key": key, "items": list(filter(lambda x: len(x) == key, words))} for key in values]
    all_item_words: set[str] = set(item.split(" "))  # reduce all words
    # all words with more than 4 can have distance 2, all other 1

    for item_word in all_item_words:
        if item_word in words:
            continue

        length = len(item_word)
        items = [x.get("items") for x in grouped_replace_words if length - 2 <= cast(int, x.get("key")) <= length + 2]
        if not items:
            continue

        all_words_to_check: Any = reduce(lambda x, y: cast(str, x) + cast(str, y), items)

        for w in all_words_to_check:
            if len(item_word) < 4 and _levenshtein(item_word, w) == 1:
                item = item.replace(item_word, w)
            elif len(item_word) >= 4 and 1 <= _levenshtein(item_word, w) <= 2:
                item = item.replace(item_word, w)

    return item


def _levenshtein(seq1: str, seq2: str) -> int:
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1,
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1,
                )

    return matrix[size_x - 1, size_y - 1]
