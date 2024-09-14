from unittest import TestCase

from talking_equipment_sdk.data import FrequencyData


class FrequencyTests(TestCase):
    def setUp(self):
        self.frequency = FrequencyData(23.4)
        self.frequency_from_int = FrequencyData(67)

    def tearDown(self):
        pass

    def test_frequency_data(self):
        self.assertEqual(self.frequency.value, 23.4)
        self.assertEqual(self.frequency_from_int.value, 67)

