import unittest
import model.utils as utils


class TestUtils(unittest.TestCase):
    def test_parse_box_office(self):
        v1 = utils.parse_box_office("300.0")
        v2 = utils.parse_box_office("7,237,794")
        v3 = utils.parse_box_office("7 million")
        v4 = utils.parse_box_office("7 billion")

        self.assertEqual(v1, 300.0)
        self.assertEqual(v2, 7237794)
        self.assertEqual(v3, 7000000)
        self.assertEqual(v4, 7000000000)
        self.assertRaises(ValueError, utils.parse_box_office, "¥300.0")

    def test_get_readable_string_from_int(self):
        v1 = utils.get_readable_string_from_int(300.0)
        v2 = utils.get_readable_string_from_int(72374)
        v3 = utils.get_readable_string_from_int(7000000)
        v4 = utils.get_readable_string_from_int(7000000000)

        self.assertEqual(v1, "$300.0")
        self.assertEqual(v2, "$72.4 thousand")
        self.assertEqual(v3, "$7.0 million")
        self.assertEqual(v4, "$7.0 billion")

    def test_parse_string_to_list(self):
        parse_list = utils.parse_string_to_list("English[2]\nItaly")
        self.assertEqual(parse_list, ["English", "Italy"])

    def test_select_top_k(self):
        res1 = utils.select_top_k([1, 2, 3], 4)
        res2 = utils.select_top_k([1, 2, 3], 2)

        self.assertEqual(res1, [1, 2, 3])
        self.assertEqual(res2, [1, 2])

    def test_select_bottom_k(self):
        res1 = utils.select_bottom_k([1, 2, 3], 5)
        res2 = utils.select_bottom_k([1, 2, 3, 4, 5], 2)

        self.assertEqual(res1, [1, 2, 3])
        self.assertEqual(res2, [3, 4])

if __name__ == "__main__":
    unittest.main()
