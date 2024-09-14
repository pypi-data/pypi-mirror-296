from unittest import TestCase

from talking_equipment_sdk.data.current.data import CurrentData, ThreePhaseCurrentData
from talking_equipment_sdk.data.data import DataModelContainer
from talking_equipment_sdk.data.frequency.data import FrequencyData
from talking_equipment_sdk.data.power_factor.data import PowerFactorData, ThreePhasePowerFactorData
from talking_equipment_sdk.data.power_meter.tests.test_power_meter import TestPowerMeter
from talking_equipment_sdk.data.total_harmonic_distortion.data import TotalHarmonicDistortionData
from talking_equipment_sdk.data.voltage.data import VoltageData, ThreePhaseVoltageData
from talking_equipment_sdk.data.volt_amps.data import VoltAmpsData, ThreePhaseVoltAmpsData, VoltAmpsReactiveData, ThreePhaseVoltAmpsReactiveData
from talking_equipment_sdk.data.watts.data import WattsData, ThreePhaseWattsData

from talking_equipment_sdk.data import ThreePhasePowerMeterData


class TestThreePhasePowerMeter(TestPowerMeter):
    def test_with_data_classes(self):
        three_phase_power_meter = ThreePhasePowerMeterData(
            current=ThreePhaseCurrentData(1.0, 2.0, 3.0),
            power_factor=ThreePhasePowerFactorData(0.5, 0.6, 0.7),
            voltage=ThreePhaseVoltageData(240.0, 120.0, 60.0),
            voltamps=ThreePhaseVoltAmpsData(1000.0, 500.0, 300.0),
            voltamps_reactive=ThreePhaseVoltAmpsReactiveData(500.0, 300.0, 100.0),
            watts=ThreePhaseWattsData(500.0, 300.0, 100.0),
            frequency=FrequencyData(59),
            total_voltamps_reactive=VoltAmpsReactiveData(300),
            total_apparent_power=WattsData(1000),
            total_power_factor=PowerFactorData(0.5),
            total_system_power=WattsData(500),
            total_harmonic_distortion=TotalHarmonicDistortionData(0.5),
            neutral_current=CurrentData(1.5),
        )

        self.assertEqual(three_phase_power_meter.current.a.value, 1.0)
        self.assertEqual(three_phase_power_meter.current.b.value, 2.0)
        self.assertEqual(three_phase_power_meter.current.c.value, 3.0)

        self.assertEqual(three_phase_power_meter.power_factor.a.value, 0.5)
        self.assertEqual(three_phase_power_meter.power_factor.b.value, 0.6)
        self.assertEqual(three_phase_power_meter.power_factor.c.value, 0.7)

        self.assertEqual(three_phase_power_meter.voltage.a.value, 240.0)
        self.assertEqual(three_phase_power_meter.voltage.b.value, 120.0)
        self.assertEqual(three_phase_power_meter.voltage.c.value, 60.0)

        self.assertEqual(three_phase_power_meter.voltamps.a.value, 1000.0)
        self.assertEqual(three_phase_power_meter.voltamps.b.value, 500.0)
        self.assertEqual(three_phase_power_meter.voltamps.c.value, 300.0)

        self.assertEqual(three_phase_power_meter.voltamps_reactive.a.value, 500.0)
        self.assertEqual(three_phase_power_meter.voltamps_reactive.b.value, 300.0)
        self.assertEqual(three_phase_power_meter.voltamps_reactive.c.value, 100.0)

        self.assertEqual(three_phase_power_meter.watts.a.value, 500.0)
        self.assertEqual(three_phase_power_meter.watts.b.value, 300.0)
        self.assertEqual(three_phase_power_meter.watts.c.value, 100.0)

        self.assert_power_meter(three_phase_power_meter)



