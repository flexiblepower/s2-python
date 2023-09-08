from s2python.common import CommodityQuantity, Commodity


def commodity_has_quantity(commodity: 'Commodity', quantity: CommodityQuantity) -> bool:
    if commodity == Commodity.HEAT:
        return quantity in [CommodityQuantity.HEAT_THERMAL_POWER,
                            CommodityQuantity.HEAT_TEMPERATURE,
                            CommodityQuantity.HEAT_FLOW_RATE]
    elif commodity == Commodity.ELECTRICITY:
        return quantity in [CommodityQuantity.ELECTRIC_POWER_3_PHASE_SYMMETRIC,
                            CommodityQuantity.ELECTRIC_POWER_L1,
                            CommodityQuantity.ELECTRIC_POWER_L2,
                            CommodityQuantity.ELECTRIC_POWER_L3]
    elif commodity == Commodity.GAS:
        return quantity in [CommodityQuantity.NATURAL_GAS_FLOW_RATE]
    elif commodity == Commodity.OIL:
        return quantity in [CommodityQuantity.OIL_FLOW_RATE]
    else:
        raise RuntimeError(f'Unsupported commodity {commodity}. Missing implementation.')
