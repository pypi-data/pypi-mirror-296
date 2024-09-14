from unittest import TestCase

from talking_equipment_sdk import VoltageData, ThreePhaseVoltageData, ThreePhasePowerMeterData, FrequencyData, \
    VoltAmpsReactiveData, WattsData, PowerFactorData, CurrentData, ThreePhaseCurrentData, ThreePhaseWattsData, \
    ThreePhasePowerFactorData, TotalHarmonicDistortionData


class TestSerialization(TestCase):
    def setUp(self):
        self.voltage = VoltageData(23.4)
        self.three_phase_voltage = ThreePhaseVoltageData(34.5, 45.6, 56)
        self.three_phase_power_meter = ThreePhasePowerMeterData(
            frequency=FrequencyData(
                1.0
            ),
            total_voltamps_reactive=VoltAmpsReactiveData(
                1.1
            ),
            total_apparent_power=WattsData(
                1.2
            ),
            total_power_factor=PowerFactorData(
                1.3
            ),
            total_system_power=WattsData(
                1.4
            ),
            neutral_current=CurrentData(
                1.5
            ),
            voltage=ThreePhaseVoltageData(
                a=1.6,
                b=1.7,
                c=1.8,
            ),
            current=ThreePhaseCurrentData(
                a=1.9,
                b=1.10,
                c=1.11
            ),
            watts=ThreePhaseWattsData(
                a=1.12,
                b=1.13,
                c=1.14
            ),
            power_factor=ThreePhasePowerFactorData(
                a=1.15,
                b=1.16,
                c=1.17
            ),
            total_harmonic_distortion=TotalHarmonicDistortionData(
                1.18
            ),
        )

    def test_dump(self):
        self.assertEqual(self.voltage.model_dump()['value'], 23.4)
        self.assertEqual(self.three_phase_voltage.model_dump()['a']['value'], 34.5)

    def test_dump_json(self):
        self.assertTrue(isinstance(self.voltage.model_dump_json(), str))
        self.assertTrue(isinstance(self.three_phase_voltage.model_dump_json(), str))

    def test_value_dump(self):
        self.assertTrue(isinstance(self.voltage.value, float))
        self.assertTrue(isinstance(self.three_phase_voltage.value, str))

    def test_validate(self):
        three_phase_voltage_dict = self.three_phase_voltage.model_dump()
        new_three_phase_voltage =  ThreePhaseVoltageData.model_validate(three_phase_voltage_dict)

        self.assertEqual(new_three_phase_voltage.b.value, 45.6)

    def test_validate_json(self):
        three_phase_voltage_json_data = self.three_phase_voltage.value
        new_three_phase_voltage =  ThreePhaseVoltageData.model_validate_json(three_phase_voltage_json_data)

        self.assertEqual(new_three_phase_voltage.c.value, 56.0)

    def test_large_validate(self):
        three_phase_power_meter_dict = self.three_phase_power_meter.model_dump()
        new_three_phase_power_meter =  ThreePhasePowerMeterData.model_validate(three_phase_power_meter_dict)

        self.assertEqual(new_three_phase_power_meter.current.c.value, 1.11)

    def test_large_validate_json(self):
        three_phase_power_meter_json = self.three_phase_power_meter.value
        new_three_phase_power_meter =  ThreePhasePowerMeterData.model_validate_json(three_phase_power_meter_json)

        self.assertEqual(new_three_phase_power_meter.current.c.value, 1.11)

