# generated by datamodel-codegen:
#   filename:  openapi.yml
#   timestamp: 2023-05-10T12:40:33+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field, conint, constr


class RoleType(Enum):
    ENERGY_PRODUCER = 'ENERGY_PRODUCER'
    ENERGY_CONSUMER = 'ENERGY_CONSUMER'
    ENERGY_STORAGE = 'ENERGY_STORAGE'


class Commodity(Enum):
    GAS = 'GAS'
    HEAT = 'HEAT'
    ELECTRICITY = 'ELECTRICITY'
    OIL = 'OIL'


class NumberRange(BaseModel):
    class Config:
        extra = Extra.forbid

    start_of_range: float = Field(
        ..., description='Number that defines the start of the range'
    )
    end_of_range: float = Field(
        ..., description='Number that defines the end of the range'
    )


class CommodityQuantity(Enum):
    ELECTRIC_POWER_L1 = 'ELECTRIC.POWER.L1'
    ELECTRIC_POWER_L2 = 'ELECTRIC.POWER.L2'
    ELECTRIC_POWER_L3 = 'ELECTRIC.POWER.L3'
    ELECTRIC_POWER_3_PHASE_SYMMETRIC = 'ELECTRIC.POWER.3_PHASE_SYMMETRIC'
    NATURAL_GAS_FLOW_RATE = 'NATURAL_GAS.FLOW_RATE'
    HYDROGEN_FLOW_RATE = 'HYDROGEN.FLOW_RATE'
    HEAT_TEMPERATURE = 'HEAT.TEMPERATURE'
    HEAT_FLOW_RATE = 'HEAT.FLOW_RATE'
    HEAT_THERMAL_POWER = 'HEAT.THERMAL_POWER'
    OIL_FLOW_RATE = 'OIL.FLOW_RATE'


class ID(BaseModel):
    __root__: constr(regex=r'[a-zA-Z0-9\-_:]{2,64}') = Field(
        ..., description='An identifier expressed as a UUID'
    )


class Duration(BaseModel):
    __root__: conint(ge=0) = Field(..., description='Duration in milliseconds')


class Timer(BaseModel):
    class Config:
        extra = Extra.forbid

    id: ID = Field(
        ...,
        description='ID of the Timer. Must be unique in the scope of the OMBC.SystemDescription, FRBC.ActuatorDescription or DDBC.ActuatorDescription in which it is used.',
    )
    diagnostic_label: Optional[str] = Field(
        None,
        description='Human readable name/description of the Timer. This element is only intended for diagnostic purposes and not for HMI applications.',
    )
    duration: Duration = Field(
        ...,
        description='The time it takes for the Timer to finish after it has been started',
    )


class Role(BaseModel):
    class Config:
        extra = Extra.forbid

    role: RoleType = Field(
        ..., description='Role type of the Resource Manager for the given commodity'
    )
    commodity: Commodity = Field(..., description='Commodity the role refers to.')


class PowerRange(BaseModel):
    class Config:
        extra = Extra.forbid

    start_of_range: float = Field(
        ..., description='Power value that defines the start of the range.'
    )
    end_of_range: float = Field(
        ..., description='Power value that defines the end of the range.'
    )
    commodity_quantity: CommodityQuantity = Field(
        ..., description='The power quantity the values refer to'
    )


class Transition(BaseModel):
    class Config:
        extra = Extra.forbid

    id: ID = Field(
        ...,
        description='ID of the Transition. Must be unique in the scope of the OMBC.SystemDescription, FRBC.ActuatorDescription or DDBC.ActuatorDescription in which it is used.',
    )
    from_: ID = Field(
        ...,
        alias='from',
        description='ID of the OperationMode (exact type differs per ControlType) that should be switched from.',
    )
    to: ID = Field(
        ...,
        description='ID of the OperationMode (exact type differs per ControlType) that will be switched to.',
    )
    start_timers: List[ID] = Field(
        ...,
        description='List of IDs of Timers that will be (re)started when this transition is initiated',
        max_items=1000,
        min_items=0,
    )
    blocking_timers: List[ID] = Field(
        ...,
        description='List of IDs of Timers that block this Transition from initiating while at least one of these Timers is not yet finished',
        max_items=1000,
        min_items=0,
    )
    transition_costs: Optional[float] = Field(
        None,
        description='Absolute costs for going through this Transition in the currency as described in the ResourceManagerDetails.',
    )
    transition_duration: Optional[Duration] = Field(
        None,
        description='Indicates the time between the initiation of this Transition, and the time at which the device behaves according to the Operation Mode which is defined in the ‘to’ data element. When no value is provided it is assumed the transition duration is negligible.',
    )
    abnormal_condition_only: bool = Field(
        ...,
        description='Indicates if this Transition may only be used during an abnormal condition (see Clause )',
    )


class FRBCOperationModeElement(BaseModel):
    class Config:
        extra = Extra.forbid

    fill_level_range: NumberRange = Field(
        ...,
        description='The range of the fill level for which this FRBC.OperationModeElement applies. The start of the NumberRange shall be smaller than the end of the NumberRange.',
    )
    fill_rate: NumberRange = Field(
        ...,
        description='Indicates the change in fill_level per second. The lower_boundary of the NumberRange is associated with an operation_mode_factor of 0, the upper_boundary is associated with an operation_mode_factor of 1. ',
    )
    power_ranges: List[PowerRange] = Field(
        ...,
        description='The power produced or consumed by this operation mode. The start of each PowerRange is associated with an operation_mode_factor of 0, the end is associated with an operation_mode_factor of 1. In the array there must be at least one PowerRange, and at most one PowerRange per CommodityQuantity.',
        max_items=10,
        min_items=1,
    )
    running_costs: Optional[NumberRange] = Field(
        None,
        description='Additional costs per second (e.g. wear, services) associated with this operation mode in the currency defined by the ResourceManagerDetails, excluding the commodity cost. The range is expressing uncertainty and is not linked to the operation_mode_factor.',
    )


class FRBCOperationMode(BaseModel):
    class Config:
        extra = Extra.forbid

    id: ID = Field(
        ...,
        description='ID of the FRBC.OperationMode. Must be unique in the scope of the FRBC.ActuatorDescription in which it is used.',
    )
    diagnostic_label: Optional[str] = Field(
        None,
        description='Human readable name/description of the FRBC.OperationMode. This element is only intended for diagnostic purposes and not for HMI applications.',
    )
    elements: List[FRBCOperationModeElement] = Field(
        ...,
        description='List of FRBC.OperationModeElements, which describe the properties of this FRBC.OperationMode depending on the fill_level. The fill_level_ranges of the items in the Array must be contiguous.',
        max_items=100,
        min_items=1,
    )
    abnormal_condition_only: bool = Field(
        ...,
        description='Indicates if this FRBC.OperationMode may only be used during an abnormal condition',
    )


class FRBCActuatorDescription(BaseModel):
    class Config:
        extra = Extra.forbid

    id: ID = Field(
        ...,
        description='ID of the Actuator. Must be unique in the scope of the Resource Manager, for at least the duration of the session between Resource Manager and CEM.',
    )
    diagnostic_label: Optional[str] = Field(
        None,
        description='Human readable name/description for the actuator. This element is only intended for diagnostic purposes and not for HMI applications.',
    )
    supported_commodities: List[Commodity] = Field(
        ..., description='List of all supported Commodities.', max_items=4, min_items=1
    )
    operation_modes: List[FRBCOperationMode] = Field(
        ...,
        description='Provided FRBC.OperationModes associated with this actuator',
        max_items=100,
        min_items=1,
    )
    transitions: List[Transition] = Field(
        ...,
        description='Possible transitions between FRBC.OperationModes associated with this actuator.',
        max_items=1000,
        min_items=0,
    )
    timers: List[Timer] = Field(
        ...,
        description='List of Timers associated with this actuator',
        max_items=1000,
        min_items=0,
    )
