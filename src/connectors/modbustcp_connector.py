import pyModbusTCP.client
import pyModbusTCP.utils

from ..fldlogging import log


def _get_only_16bit_address_from_full_address(full_address: int) -> int:
    return int(str(hex(full_address-int(full_address/10000)*10000-1)).split('x')[1], 16)


class ModbusTCPConnector:
    _pymodbustcp = None

    def __init__(self, ip_address: str, port: int, unit_it: int = 1, auto_open: bool = True, auto_close: bool = True, debug_rx_tx: bool = False):
        self._pymodbustcp = pyModbusTCP.client.ModbusClient(host=ip_address, port=port, unit_id=unit_it, auto_open=auto_open, auto_close=auto_close, debug=debug_rx_tx)

    def _read_float(self, only_16bit_address: int, size: int = 1, input_true_holding_false: bool = False) -> (list[float], None):
        """
        Reference to:
        https://pymodbustcp.readthedocs.io/en/latest/examples/client_float.html
        Read float(s) with registers.
        """
        if not input_true_holding_false:  # Holding register
            reg_l = self._pymodbustcp.read_holding_registers(only_16bit_address, size)
        else:  # Input register
            reg_l = self._pymodbustcp.read_input_registers(only_16bit_address, size)
        if reg_l:
            return [pyModbusTCP.utils.decode_ieee(f) for f in pyModbusTCP.utils.word_list_to_long(reg_l)]
        else:
            return None

    def _read_register(self, address: int, number_of_registers_to_read_from: int = 1, data_type: type = int, input_true_holding_false: bool = False) -> (list[int], list[float], None):

        result = None

        if address < 10000:  # Only register address
            if data_type == float:
                result = self._read_float(address, number_of_registers_to_read_from, input_true_holding_false)
            elif data_type == int:
                if input_true_holding_false:
                    result = self._pymodbustcp.read_input_registers(address, number_of_registers_to_read_from)
                else:
                    result = self._pymodbustcp.read_holding_registers(address, number_of_registers_to_read_from)
            else:
                log(error='data_type not requestable')
                return None

        # Not just register address
        elif 30001 <= address <= 39999:  # Input register
            addr_hex = _get_only_16bit_address_from_full_address(address)
            result = self._read_register(addr_hex, number_of_registers_to_read_from, data_type, True)
        elif 40001 <= address <= 49999:  # Holding register
            addr_hex = _get_only_16bit_address_from_full_address(address)
            result = self._read_register(addr_hex, number_of_registers_to_read_from, data_type, False)
        else:
            log(error='address out of range')
            return None

        if result is None:
            log(alert='Result of reading register is empty')

        return result

    def read_input_register(self, address: int, number_of_registers_to_read_from: int = 1, data_type: type = int) -> (list[int], list[float], None):
        return self._read_register(address, number_of_registers_to_read_from, data_type, True)

    def read_holding_register(self, address: int, number_of_registers_to_read_from: int = 1, data_type: type = int) -> (list[int], list[float], None):
        return self._read_register(address, number_of_registers_to_read_from, data_type, False)

    def _read_bit(self, address: int, number_of_registers_to_read_from: int = 1, coil_true_discrete_false: bool = False) -> (list[bool], None):

        result = None

        addr_hex = _get_only_16bit_address_from_full_address(address)

        if coil_true_discrete_false:
            result = self._pymodbustcp.read_coils(addr_hex, number_of_registers_to_read_from)
        else:
            result = self._pymodbustcp.read_discrete_inputs(addr_hex, number_of_registers_to_read_from)

        if result is None:
            log(alert='Result of reading bit is empty')

        return result

    def read_coil(self, address: int, number_of_registers_to_read_from: int = 1) -> (list[bool], None):
        return self._read_bit(address, number_of_registers_to_read_from, False)

    def read_discrete(self, address: int, number_of_registers_to_read_from: int = 1) -> (list[bool], None):
        return self._read_bit(address, number_of_registers_to_read_from, True)

    def _write_float(self, only_16bit_address: int, floats_list: list[float]) -> bool:
        """
        Returns: True if write ok

        Reference to:
        https://pymodbustcp.readthedocs.io/en/latest/examples/client_float.html
        float(s) with write multiple registers.
        """
        b32_l = [pyModbusTCP.utils.encode_ieee(f) for f in floats_list]
        b16_l = pyModbusTCP.utils.long_list_to_word(b32_l)
        return self._pymodbustcp.write_multiple_registers(only_16bit_address, b16_l)

    def write_coil(self, address: int, values: (bool, list[bool])) -> bool:
        """
        Returns: True if write ok
        """

        addr_hex = _get_only_16bit_address_from_full_address(address)

        if type(values) == bool:
            return self._pymodbustcp.write_single_coil(addr_hex, values)
        elif type(values) == list[bool]:
            return self._pymodbustcp.write_multiple_coils(addr_hex, values)
        else:
            log(error='Could not write coil: Type of values is not bool or list[bool] but ' + str(type(values)))
            return False

    def write_holding_register(self, address, values: (int, float, list)) -> bool:
        """
        Returns: True if write ok
        """

        if address < 10000:  # Only register address
            if type(values) == float:
                return self._write_float(address, list(values))
            elif type(values) == list[float]:
                return self._write_float(address, values)
            elif type(values) == int:
                return self._pymodbustcp.write_single_register(address, values)
            elif type(values) == list[int]:
                return self._pymodbustcp.write_single_register(address, values)
            elif type(values) == list[int, float]:
                addr = address
                result = True
                for value in values:
                    result = self.write_holding_register(addr, value)
                    if not result:
                        log(error='Writing holding register failed at address ' + str(addr) + 'with value ' + str(value))
                        return False
                    if type(value) == int:
                        addr += 1
                    if type(value) == float:
                        addr += 2
                return result
            else:
                log(error='data_type not writeable: ' + str(type(values)))
                return False

        # Not just register address
        elif 30001 <= address <= 39999:  # Input register
            log(error='Tried to write to input register but that one is read only')
            return False
        elif 40001 <= address <= 49999:  # Holding register
            addr_hex = _get_only_16bit_address_from_full_address(address)
            return self.write_holding_register(addr_hex, values)
        else:
            log(error='address out of range')
            return False
