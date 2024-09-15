import unittest
from dtreg.extract_orkg import extract_orkg


class TestExtractOrkg(unittest.TestCase):

    def test_extract_orkg(self):
        result = extract_orkg("https://incubating.orkg.org/template/R937648")
        expected = {'measurement_scale': [[{'dt_name': 'measurement_scale',
                                            'dt_id': 'R937648',
                                            'dt_class': 'C75002'}],
                                          [{
                                              "dtp_name": "label",
                                              "dtp_id": "label",
                                              "dtp_card_min": 0,
                                              "dtp_card_max": 1,
                                              "dtp_value_type": "string"}]]}
        self.assertEqual(result, expected)

    def test_extract_orkg_props(self):
        schema = extract_orkg("https://incubating.orkg.org/template/R855534")
        values = schema["inferential_test_output"][1][0].values()
        expected = "dict_values(['has_format', 'P114000', 1, None, 'Table'])"
        self.assertEqual(str(values), expected)

    def test_extract_orkg_nested(self):
        schema = extract_orkg("https://incubating.orkg.org/template/R903086")
        expected = "dict_keys(['statistical_variable', 'sample_size', 'data_input'])"
        self.assertEqual(str(schema.keys()), expected)


if __name__ == '__main__':
    unittest.main()
