from unittest import TestCase

from talking_equipment_sdk.data import TotalHarmonicDistortionData, ThreePhaseTotalHarmonicDistortionData


class TotalHarmonicDistortionTests(TestCase):
    def setUp(self):
        self.total_harmonic_distortion = TotalHarmonicDistortionData(23.4)
        self.total_harmonic_distortion_from_int = TotalHarmonicDistortionData(67)
        self.three_phase_total_harmonic_distortion = ThreePhaseTotalHarmonicDistortionData(a=34.5, b=TotalHarmonicDistortionData(45.6), c=56)

    def tearDown(self):
        pass

    def test_total_harmonic_distortion_data(self):
        self.assertEqual(self.total_harmonic_distortion.value, 23.4)
        self.assertEqual(self.total_harmonic_distortion_from_int.value, 67)

    def test_three_phase_total_harmonic_distortion_data(self):
        self.assertEqual(self.three_phase_total_harmonic_distortion.a.value, 34.5)
        self.assertEqual(self.three_phase_total_harmonic_distortion.b.value, 45.6)
        self.assertEqual(self.three_phase_total_harmonic_distortion.c.value, 56.0)