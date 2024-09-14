from unittest import TestCase

from talking_equipment_sdk.data import VoltageData, ThreePhaseVoltageData


class VoltageTests(TestCase):
    def setUp(self):
        self.voltage = VoltageData(23.4)
        self.voltage_from_int = VoltageData(67)
        self.three_phase_voltage = ThreePhaseVoltageData(a=34.5, b=VoltageData(45.6), c=56)

    def tearDown(self):
        pass

    def test_voltage_data(self):
        self.assertEqual(self.voltage.value, 23.4)
        self.assertEqual(self.voltage_from_int.value, 67)

    def test_three_phase_voltage_data(self):
        self.assertEqual(self.three_phase_voltage.a.value, 34.5)
        self.assertEqual(self.three_phase_voltage.b.value, 45.6)
        self.assertEqual(self.three_phase_voltage.c.value, 56.0)