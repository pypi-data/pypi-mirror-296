from unittest import TestCase

from talking_equipment_sdk.data import PowerFactorData, ThreePhasePowerFactorData


class PowerFactorTests(TestCase):
    def setUp(self):
        self.power_factor = PowerFactorData(23.4)
        self.power_factor_from_int = PowerFactorData(67)
        self.three_phase_power_factor = ThreePhasePowerFactorData(a=34.5, b=PowerFactorData(45.6), c=56)

    def tearDown(self):
        pass

    def test_power_factor_data(self):
        self.assertEqual(self.power_factor.value, 23.4)
        self.assertEqual(self.power_factor_from_int.value, 67)

    def test_three_phase_power_factor_data(self):
        self.assertEqual(self.three_phase_power_factor.a.value, 34.5)
        self.assertEqual(self.three_phase_power_factor.b.value, 45.6)
        self.assertEqual(self.three_phase_power_factor.c.value, 56.0)