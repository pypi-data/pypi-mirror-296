import unittest
from dtreg.load_datatype import load_datatype


class TestLoadDatatype(unittest.TestCase):

    def test_load_nonstatic(self):
        dt = load_datatype("https://doi.org/21.T11969/1ea0e148d9bbe08335cd")
        self.assertEqual(next(iter(dt.__dict__)), 'pidinst_schemaobject')

    def test_load_prop_epic(self):
        dt = load_datatype("https://doi.org/21.T11969/74bc7748b8cd520908bc")
        props = dt.inferential_test_output.prop_list
        expected = ['label', 'has_description', 'comment', 'has_format']
        self.assertEqual(props, expected)

    def test_load_prop_orkg(self):
        dt = load_datatype("https://incubating.orkg.org/template/R855534")
        props = dt.inferential_test_output.prop_list
        expected = ['has_format', 'has_description', 'comment', "label"]
        self.assertEqual(props, expected)


if __name__ == '__main__':
    unittest.main()
