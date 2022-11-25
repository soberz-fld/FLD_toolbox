from ..connectors.homeassistant_connector import HomeAssistantConnector
from ..connectors.modbustcp_connector import ModbusTCPConnector

from ..fldlogging import log


class ModbusTcpHomeAssistantGateway(ModbusTCPConnector):
    def __init__(self, homeassistant_connector: HomeAssistantConnector, modbustcp_ip_address: str, modbustcp_port: int, modbustcp_unit_it: int = 1, modbustcp_auto_open: bool = True, modbustcp_auto_close: bool = True, modbustcp_debug_rx_tx: bool = False):
        super().__init__(modbustcp_ip_address, modbustcp_port, modbustcp_unit_it, modbustcp_auto_open, modbustcp_auto_close, modbustcp_debug_rx_tx)
        self._homeassistant_connector = homeassistant_connector

    def modbus_register_to_homeassistant(self, mb_address: int, mb_number_of_registers_to_read_from: int, mb_data_type: type, ha_entity_id: str, ha_unit_of_measurement: str = '', ha_device_class: str = '', ha_friendly_name: str = '', **ha_attributes) -> bool:
        result = self.read_input_register(mb_address, mb_number_of_registers_to_read_from, mb_data_type)

        attr = dict()
        if ha_unit_of_measurement != '':
            attr['unit_of_measurement'] = ha_unit_of_measurement
        if ha_device_class != '':
            attr['device_class'] = ha_device_class
        if ha_friendly_name != '':
            attr['friendly_name'] = ha_friendly_name
        for kv in ha_attributes:
            attr[kv] = ha_attributes[kv]

        if result:
            return self._homeassistant_connector.post_state(ha_entity_id, result.__round__(2), attr)
        else:
            log(error='Result empty')
            return False
