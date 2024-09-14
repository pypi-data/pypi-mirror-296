from unittest import TestCase

from talking_equipment_sdk.data.power_meter.data import _PowerMeterData


class TestPowerMeter(TestCase):
    def assert_power_meter(self, power_meter: _PowerMeterData) -> bool:
        self.assertEqual(power_meter.frequency.value, 59)
        self.assertEqual(power_meter.total_voltamps_reactive.value, 300)
        self.assertEqual(power_meter.total_apparent_power.value, 1000)
        self.assertEqual(power_meter.total_power_factor.value, 0.5)
        self.assertEqual(power_meter.total_system_power.value, 500)
        self.assertEqual(power_meter.total_harmonic_distortion.value, 0.5)
        self.assertEqual(power_meter.neutral_current.value, 1.5)
