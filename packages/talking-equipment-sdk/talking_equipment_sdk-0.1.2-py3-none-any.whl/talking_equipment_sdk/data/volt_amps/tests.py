from unittest import TestCase

from talking_equipment_sdk.data import VoltAmpsData, VoltAmpsReactiveData, ThreePhaseVoltAmpsData, ThreePhaseVoltAmpsReactiveData


class VoltAmpsTests(TestCase):
    def setUp(self):
        self.voltamps = VoltAmpsData(23.4)
        self.voltamps_from_int = VoltAmpsData(67)
        self.voltamps_reactive = VoltAmpsReactiveData(23.49)
        self.voltamps_reactive_from_int = VoltAmpsReactiveData(767)
        self.three_phase_voltamps = ThreePhaseVoltAmpsData(a=34.5, b=VoltAmpsData(45.6), c=56)
        self.three_phase_voltamps_reactive = ThreePhaseVoltAmpsReactiveData(a=94.5, b=VoltAmpsReactiveData(105.6), c=256)

    def tearDown(self):
        pass

    def test_voltamps(self):
        self.assertEqual(self.voltamps.value, 23.4)
        self.assertEqual(self.voltamps_from_int.value, 67)

    def test_three_phase_voltamps(self):
        self.assertEqual(self.three_phase_voltamps.a.value, 34.5)
        self.assertEqual(self.three_phase_voltamps.b.value, 45.6)
        self.assertEqual(self.three_phase_voltamps.c.value, 56.0)

    def test_voltamps_reactive(self):
        self.assertEqual(self.voltamps_reactive.value, 23.49)
        self.assertEqual(self.voltamps_reactive_from_int.value, 767)

    def test_three_phase_voltamps_reactive(self):
        self.assertEqual(self.three_phase_voltamps_reactive.a.value, 94.5)
        self.assertEqual(self.three_phase_voltamps_reactive.b.value, 105.6)
        self.assertEqual(self.three_phase_voltamps_reactive.c.value, 256.0)