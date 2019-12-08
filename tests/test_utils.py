import tempfile
import types
from pathlib import Path
from unittest import TestCase

from crate_assessment.utils import get_files_list


class TestUtils(TestCase):

    def test_get_file_list(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            open(Path(tmpdirname, 'file1.txt'), 'w').close()
            open(Path(tmpdirname, 'file2.txt'), 'w').close()
            result = get_files_list(Path(tmpdirname))
            self.assertIsInstance(result, types.GeneratorType)
            self.assertEqual(len(list(result)), 2)
