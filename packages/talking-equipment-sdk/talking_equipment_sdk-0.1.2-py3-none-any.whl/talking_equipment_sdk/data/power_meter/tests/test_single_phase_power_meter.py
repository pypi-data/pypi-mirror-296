from talking_equipment_sdk.data.power_meter.tests.test_power_meter import TestPowerMeter

from talking_equipment_sdk.data import SinglePhasePowerMeterData
from talking_equipment_sdk.data.current.data import CurrentData
from talking_equipment_sdk.data.frequency.data import FrequencyData
from talking_equipment_sdk.data.power_factor.data import PowerFactorData
from talking_equipment_sdk.data.total_harmonic_distortion.data import TotalHarmonicDistortionData
from talking_equipment_sdk.data.volt_amps.data import VoltAmpsData, VoltAmpsReactiveData
from talking_equipment_sdk.data.voltage.data import VoltageData
from talking_equipment_sdk.data.watts.data import WattsData


class TestSinglePhasePowerMeter(TestPowerMeter):
    def test_with_data_classes(self):
        single_phase_power_meter = SinglePhasePowerMeterData(
            current=CurrentData(1.0),
            power_factor=PowerFactorData(0.5),
            voltage=VoltageData(240.0),
            voltamps=VoltAmpsData(1000.0),
            voltamps_reactive=VoltAmpsReactiveData(500.0),
            watts=WattsData(500.0),
            frequency=FrequencyData(59),
            total_voltamps_reactive=VoltAmpsReactiveData(300),
            total_apparent_power=WattsData(1000),
            total_power_factor=PowerFactorData(0.5),
            total_system_power=WattsData(500),
            total_harmonic_distortion=TotalHarmonicDistortionData(0.5),
            neutral_current=CurrentData(1.5),
        )

        self.assert_single_phase_power_meter(single_phase_power_meter)
        self.assert_power_meter(single_phase_power_meter)

    def test_with_values(self):
        single_phase_power_meter = SinglePhasePowerMeterData(
            current=1.0,
            power_factor=0.5,
            voltage=240.0,
            voltamps=1000.0,
            voltamps_reactive=500.0,
            watts=500.0,
            frequency=59,
            total_voltamps_reactive=300,
            total_apparent_power=1000,
            total_power_factor=0.5,
            total_system_power=500,
            total_harmonic_distortion=0.5,
            neutral_current=1.5,
        )

        self.assert_single_phase_power_meter(single_phase_power_meter)
        self.assert_power_meter(single_phase_power_meter)

    def assert_single_phase_power_meter(self, power_meter: SinglePhasePowerMeterData):
        self.assertEqual(power_meter.current.value, 1.0)
        self.assertEqual(power_meter.power_factor.value, 0.5)
        self.assertEqual(power_meter.voltage.value, 240.0)
        self.assertEqual(power_meter.voltamps.value, 1000.0)
        self.assertEqual(power_meter.voltamps_reactive.value, 500.0)
        self.assertEqual(power_meter.watts.value, 500.0)
