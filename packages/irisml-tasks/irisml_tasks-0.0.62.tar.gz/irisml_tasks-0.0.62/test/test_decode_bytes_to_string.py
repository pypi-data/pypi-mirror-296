import unittest
from irisml.tasks.decode_bytes_to_str import Task


class TestDecodeBytesToStr(unittest.TestCase):
    def test_simple(self):
        inputs = Task.Inputs(data=b'hello')
        outputs = Task(Task.Config()).execute(inputs)
        self.assertEqual(outputs.string, 'hello')

    def test_encoding_ascii(self):
        inputs = Task.Inputs(data=b'hello')
        outputs = Task(Task.Config(encoding='ascii')).execute(inputs)
        self.assertEqual(outputs.string, 'hello')
