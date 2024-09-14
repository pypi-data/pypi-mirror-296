import unittest
from talking_equipment_sdk.data import CounterData


class TestCounter(unittest.TestCase):

    def test_initialization(self):
        counter = CounterData(16785)
        self.assertEqual(counter.value, 16785)


