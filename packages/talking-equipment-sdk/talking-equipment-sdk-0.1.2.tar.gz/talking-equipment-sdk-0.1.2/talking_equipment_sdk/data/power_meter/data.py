from dataclasses import dataclass
from typing import Optional, Union

from pydantic import field_validator

from talking_equipment_sdk.data.current.data import CurrentData, ThreePhaseCurrentData
from talking_equipment_sdk.data.data import DataModelContainer
from talking_equipment_sdk.data.frequency.data import FrequencyData
from talking_equipment_sdk.data.power_factor.data import PowerFactorData, ThreePhasePowerFactorData
from talking_equipment_sdk.data.total_harmonic_distortion.data import TotalHarmonicDistortionData
from talking_equipment_sdk.data.voltage.data import VoltageData, ThreePhaseVoltageData
from talking_equipment_sdk.data.volt_amps.data import VoltAmpsData, ThreePhaseVoltAmpsData, VoltAmpsReactiveData, ThreePhaseVoltAmpsReactiveData
from talking_equipment_sdk.data.watts.data import WattsData, ThreePhaseWattsData


class _PowerMeterData(DataModelContainer):
    frequency: Optional[FrequencyData] = None
    total_voltamps_reactive: Optional[VoltAmpsReactiveData] = None
    total_apparent_power: Optional[WattsData] = None
    total_power_factor: Optional[PowerFactorData] = None
    total_system_power: Optional[WattsData] = None
    total_harmonic_distortion: Optional[TotalHarmonicDistortionData] = None
    neutral_current: Optional[CurrentData] = None

    def __init__(
            self,
            frequency: Optional[Union[FrequencyData, float, int]] = None,
            total_voltamps_reactive: Optional[Union[VoltAmpsReactiveData, float, int]] = None,
            total_apparent_power: Optional[Union[WattsData, float, int]] = None,
            total_power_factor: Optional[Union[PowerFactorData, float, int]] = None,
            total_system_power: Optional[Union[WattsData, float, int]] = None,
            total_harmonic_distortion: Optional[Union[TotalHarmonicDistortionData, float, int]] = None,
            neutral_current: Optional[Union[CurrentData, float, int]] = None,
            **kwargs,
    ):
        super().__init__(
            frequency=self._convert_value(frequency, FrequencyData),
            total_voltamps_reactive=self._convert_value(total_voltamps_reactive, VoltAmpsReactiveData),
            total_apparent_power=self._convert_value(total_apparent_power, WattsData),
            total_power_factor=self._convert_value(total_power_factor, PowerFactorData),
            total_system_power=self._convert_value(total_system_power, WattsData),
            total_harmonic_distortion=self._convert_value(total_harmonic_distortion, TotalHarmonicDistortionData),
            neutral_current=self._convert_value(neutral_current, CurrentData),
            **kwargs,
        )




class SinglePhasePowerMeterData(_PowerMeterData):
    current: Optional[CurrentData] = None
    power_factor: Optional[PowerFactorData] = None
    voltage: Optional[VoltageData] = None
    voltamps: Optional[VoltAmpsData] = None
    voltamps_reactive: Optional[VoltAmpsReactiveData] = None
    watts: Optional[WattsData] = None

    def __init__(
            self,
            current: Optional[Union[CurrentData, float, int]] = None,
            power_factor: Optional[Union[PowerFactorData, float, int]] = None,
            voltage: Optional[Union[VoltageData, float, int]] = None,
            voltamps: Optional[Union[VoltAmpsData, float, int]] = None,
            voltamps_reactive: Optional[Union[VoltAmpsReactiveData, float, int]] = None,
            watts: Optional[Union[WattsData, float, int]] = None,
            **kwargs
    ):
        super().__init__(
            current=self._convert_value(current, CurrentData),
            power_factor=self._convert_value(power_factor, PowerFactorData),
            voltage=self._convert_value(voltage, VoltageData),
            voltamps=self._convert_value(voltamps, VoltAmpsData),
            voltamps_reactive=self._convert_value(voltamps_reactive, VoltAmpsReactiveData),
            watts=self._convert_value(watts, WattsData),
            **kwargs
        )


class ThreePhasePowerMeterData(_PowerMeterData):
    current: Optional[ThreePhaseCurrentData] = None
    power_factor: Optional[ThreePhasePowerFactorData] = None
    voltage: Optional[ThreePhaseVoltageData] = None
    voltamps: Optional[ThreePhaseVoltAmpsData] = None
    voltamps_reactive: Optional[ThreePhaseVoltAmpsReactiveData] = None
    watts: Optional[ThreePhaseWattsData] = None

    def __init__(
            self,
            current: Optional[ThreePhaseCurrentData] = None,
            power_factor: Optional[ThreePhasePowerFactorData] = None,
            voltage: Optional[ThreePhaseVoltageData] = None,
            voltamps: Optional[ThreePhaseVoltAmpsData] = None,
            voltamps_reactive: Optional[ThreePhaseVoltAmpsReactiveData] = None,
            watts: Optional[ThreePhaseWattsData] = None,
            **kwargs
    ):
        super().__init__(
            current=current,
            power_factor=power_factor,
            voltage=voltage,
            voltamps=voltamps,
            voltamps_reactive=voltamps_reactive,
            watts=watts,
            **kwargs
        )
