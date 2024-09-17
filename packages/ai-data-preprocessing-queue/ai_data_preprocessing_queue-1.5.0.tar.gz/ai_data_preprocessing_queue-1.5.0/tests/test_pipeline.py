import unittest
from os import path

from ai_data_preprocessing_queue.Pipeline import Pipeline

ABS_PATH_TEST_DATA = path.join(path.dirname(path.abspath(__file__)), "test_data")


class PipelineTest(unittest.TestCase):
    def test_text_only(self) -> None:
        pipeline = Pipeline({"text_only": None})
        value = pipeline.consume('123 text - "more" text , and .')
        self.assertEqual("    text    more  text   and  ", value)

    def test_remove_numbers(self) -> None:
        pipeline = Pipeline({"remove_numbers": None})
        value = pipeline.consume('123 text - "more" text123 , and .')
        self.assertEqual('    text - "more" text    , and .', value)

    def test_remove_punctuation(self) -> None:
        pipeline = Pipeline({"remove_punctuation": None})
        value = pipeline.consume('123 text - "more" text123 , and .')
        self.assertEqual("123 text    more  text123   and  ", value)

    def test_text_to_lower(self) -> None:
        pipeline = Pipeline({"to_lower": None})
        value = pipeline.consume("This is a Test text with CamelCase")
        self.assertEqual("this is a test text with camelcase", value)

    def test_snowball_stemmer_english(self) -> None:
        pipeline = Pipeline({"language_detect": None, "snowball_stemmer": None})
        value = pipeline.consume("how can i trouble troubling troubled")
        self.assertEqual("how can i troubl troubl troubl", value)

    def test_snowball_stemmer_german(self) -> None:
        pipeline = Pipeline({"language_detect": None, "snowball_stemmer": None})
        value = pipeline.consume("Wie kann ich kategorie kategorien kategorischen kategorisch")
        self.assertEqual("wie kann ich kategori kategori kategor kategor", value)

    def test_multiple_steps(self) -> None:
        pipeline = Pipeline({"text_only": None, "to_lower": None})
        value = pipeline.consume("123 CamelCase")
        self.assertEqual("    camelcase", value)

    def test_regex_replacement_do_not_crash_for_no_data(self) -> None:
        pipeline = Pipeline({"regex_replacement": None})
        value = pipeline.consume("test text")
        self.assertEqual("test text", value)

    def test_regex_replacement(self) -> None:
        with open(path.join(ABS_PATH_TEST_DATA, "regex_replacement_testdata.csv"), "r", encoding="utf-8") as handler:
            pipeline = Pipeline({"regex_replacement": handler.read()})
        # date
        value = pipeline.consume("test 1.1.2019 20.2.2003 1.1.20 01.01.20 1.1.1900 1.1. 01.01. test")
        self.assertEqual(
            "test  replaceddate   replaceddate   replaceddate"
            "  replaceddate replaceddate   replaceddate  replaceddate test",
            value,
        )
        # iban
        value = pipeline.consume("test DE12500101170648489890")
        self.assertEqual("test  replacediban ", value)
        # postcode
        value = pipeline.consume("test 92637 92709 test")
        self.assertEqual("test  replacedpostcode   replacedpostcode  test", value)
        # german phone
        value = pipeline.consume("test 0961123456 test")
        self.assertEqual("test  replacedgermanphonenumber  test", value)
        value = pipeline.consume("test (0961)123456 test")
        self.assertEqual("test  replacedgermanphonenumber  test", value)
        value = pipeline.consume("test +49(0)121-79536-77 test")
        self.assertEqual("test  replacedgermanphonenumber  test", value)
        # german handy
        value = pipeline.consume("test 015125391111 test")
        self.assertEqual("test  replacedgermanphonenumber  test", value)

        # some password variation
        value = pipeline.consume("test pw test")
        self.assertEqual("test  password  test", value)
        value = pipeline.consume("test pwort test")
        self.assertEqual("test  password  test", value)
        value = pipeline.consume("test pass word test")
        self.assertEqual("test  password  test", value)

    def test_token_replacement_do_not_crash_for_no_data(self) -> None:
        pipeline = Pipeline({"token_replacement": None})
        value = pipeline.consume("test text")
        self.assertEqual("test text", value)

    def test_token_replacement(self) -> None:
        with open(path.join(ABS_PATH_TEST_DATA, "token_replacement_testdata.csv"), "r", encoding="utf-8") as handler:
            pipeline = Pipeline({"token_replacement": handler.read()})
        value = pipeline.consume("test asd bla 1212")
        self.assertEqual("test www blub 1212", value)

    def test_token_replacement_do_not_replace_parts_of_word(self) -> None:
        with open(path.join(ABS_PATH_TEST_DATA, "token_replacement_testdata.csv"), "r", encoding="utf-8") as handler:
            pipeline = Pipeline({"token_replacement": handler.read()})
        value = pipeline.consume("test abg. abgabgeschlossen 1212")
        self.assertEqual("test abgeschlossen abgabgeschlossen 1212", value)

    def test_token_replacement_also_replace_dots_at_end_of_phrase(self) -> None:
        with open(path.join(ABS_PATH_TEST_DATA, "token_replacement_testdata.csv"), "r", encoding="utf-8") as handler:
            pipeline = Pipeline({"token_replacement": handler.read()})
        value = pipeline.consume("abg. 1212")
        self.assertEqual("abgeschlossen 1212", value)

    def test_spellcheck_do_not_crash_for_no_data(self) -> None:
        pipeline = Pipeline({"spellcheck": "kopie\r\nartikel\r\n"})
        value = pipeline.consume("kopie koipe artikel artikle artilek artleki")
        self.assertEqual("kopie kopie artikel artikel artikel artleki", value)

    def test_spellcheck(self) -> None:
        pipeline = Pipeline({"spellcheck": None})
        value = pipeline.consume("kopie koipe artikel artikle artilek artleki")
        self.assertEqual("kopie koipe artikel artikle artilek artleki", value)

    def test_spellcheck_should_not_throw_exception_for_short_values(self) -> None:
        pipeline = Pipeline({"spellcheck": "kopie\r\nartikel\r\n"})
        value = pipeline.consume("k koipe artikel")
        self.assertEqual("k kopie artikel", value)


if __name__ == "__main__":
    unittest.main()
