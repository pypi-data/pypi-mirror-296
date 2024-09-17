import warnings
from typing import Any

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from nltk.stem.snowball import SnowballStemmer


lang_mapping = {"de": SnowballStemmer("german"), "en": SnowballStemmer("english")}


def step(item: Any, item_state: dict[str, Any], global_state: dict[str, Any] | None, preprocessor_data: str) -> Any:
    stemmer = lang_mapping.get(item_state["language"], lang_mapping["en"])

    stemmed_words = [stemmer.stem(word) for word in item.split()]

    return " ".join(stemmed_words)
