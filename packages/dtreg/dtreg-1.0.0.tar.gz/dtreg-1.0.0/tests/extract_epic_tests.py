import unittest
from dtreg.extract_epic import extract_epic


class TestExtractEpic(unittest.TestCase):

    def test_extract_epic(self):
        result = extract_epic("https://doi.org/21.T11969/1ea0e148d9bbe08335cd")
        expected = {'pidinst_schemaobject': [[{'dt_name': 'pidinst_schemaobject',
                                               'dt_id': '1ea0e148d9bbe08335cd',
                                               'dt_class': 'Object'}],
                                             []]}
        self.assertEqual(result, expected)

    def test_extract_epic_props(self):
        schema = extract_epic("https://doi.org/21.T11969/74bc7748b8cd520908bc")
        values = schema["inferential_test_output"][1][0].values()
        expected = "dict_values(['label', '21.T11969/74bc7748b8cd520908bc#label', 1, 1, '21.T11969/3df63b7acb0522da685d'])"
        self.assertEqual(str(values), expected)


if __name__ == '__main__':
    unittest.main()
