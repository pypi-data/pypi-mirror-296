from unittest import TestCase

from talking_equipment_sdk.data import WattsData, ThreePhaseWattsData, WattHoursData, ThreePhaseWattHoursData


class WattsTests(TestCase):
    def setUp(self):
        self.watts = WattsData(23.4)
        self.watts_from_int = WattsData(67)
        self.watt_hours = WattHoursData(23.99)
        self.watt_hours_from_int = WattHoursData(767)
        self.three_phase_watts = ThreePhaseWattsData(a=34.5, b=WattsData(45.6), c=56)
        self.three_phase_watt_hours = ThreePhaseWattHoursData(a=994.5, b=WattHoursData(55.6), c=5536)
    def tearDown(self):
        pass

    def test_watts_data(self):
        self.assertEqual(self.watts.value, 23.4)
        self.assertEqual(self.watts_from_int.value, 67)

    def test_three_phase_watts_data(self):
        self.assertEqual(self.three_phase_watts.a.value, 34.5)
        self.assertEqual(self.three_phase_watts.b.value, 45.6)
        self.assertEqual(self.three_phase_watts.c.value, 56.0)

    def test_watt_hours_data(self):
        self.assertEqual(self.watt_hours.value, 23.99)
        self.assertEqual(self.watt_hours_from_int.value, 767)

    def test_three_phase_watt_hours_data(self):
        self.assertEqual(self.three_phase_watt_hours.a.value, 994.5)
        self.assertEqual(self.three_phase_watt_hours.b.value, 55.6)
        self.assertEqual(self.three_phase_watt_hours.c.value, 5536.0)