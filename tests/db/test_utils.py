from unittest import TestCase

from crate_assessment.db.utils import clean_integer


class TestModels(TestCase):

    def test_clean_integer(self):
        tests = (  # value, excepted, default
            (None, None, None),
            (None, '', ''),
            (1, 1, None),
            (1, 1, ''),
            ('1', 1, None),
        )
        for value, excepted, default in tests:
            with self.subTest(value=value):
                self.assertEqual(clean_integer(value, default), excepted)
