from unittest import TestCase

from talking_equipment_sdk.data import CurrentData, ThreePhaseCurrentData


class CurrentTests(TestCase):
    def setUp(self):
        self.current = CurrentData(23.4)
        self.current_from_int = CurrentData(67)
        self.three_phase_current = ThreePhaseCurrentData(a=34.5, b=CurrentData(45.6), c=56)

    def tearDown(self):
        pass

    def test_current_data(self):
        self.assertEqual(self.current.value, 23.4)
        self.assertEqual(self.current_from_int.value, 67)

    def test_three_phase_current_data(self):
        self.assertEqual(self.three_phase_current.a.value, 34.5)
        self.assertEqual(self.three_phase_current.b.value, 45.6)
        self.assertEqual(self.three_phase_current.c.value, 56.0)