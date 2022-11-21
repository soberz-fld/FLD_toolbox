import pyModbusTCP.client
import pyModbusTCP.utils


class ModbusTCPConnector:
    _client = None

    def __init__(self, ip_address: str, port: int = 502, unit_it: int = 1, auto_open: bool = True):
        self._client = pyModbusTCP.client.ModbusClient(host=ip_address, port=port, unit_id=unit_it, auto_open=auto_open)

    def _read_float(self, address, number=1, holding_true_input_false: bool = False):
        """
        Reference to:
        https://pymodbustcp.readthedocs.io/en/latest/examples/client_float.html
        Read float(s) with read holding registers.
        """
        if holding_true_input_false:  # Holding register
            reg_l = self._client.read_holding_registers(address, number)
        else:  # Input register
            reg_l = self._client.read_input_registers(address, number)
        if reg_l:
            return [pyModbusTCP.utils.decode_ieee(f) for f in pyModbusTCP.utils.word_list_to_long(reg_l)]
        else:
            return None

    def _write_float(self, address, floats_list):
        """
        Reference to:
        https://pymodbustcp.readthedocs.io/en/latest/examples/client_float.html
        float(s) with write multiple registers.
        """
        b32_l = [pyModbusTCP.utils.encode_ieee(f) for f in floats_list]
        b16_l = pyModbusTCP.utils.long_list_to_word(b32_l)
        return self._client.write_multiple_registers(address, b16_l)

    def read_register(self, address, number_of_registers_for_value: int = 1, data_type: type = int,
                      holding_true_input_false: bool = False):
        if data_type == int:
            if holding_true_input_false:  # Holding register
                result = self._client.read_holding_registers(address, number_of_registers_for_value)
            else:  # Input register
                result = self._client.read_input_registers(address, number_of_registers_for_value)
            if result:
                if number_of_registers_for_value == 1:
                    return result[0]
                else:
                    pass  # TODO: Handling of concatenating ints: multiply by 2^(indexInArray+1) ??
            else:
                print('No result')  # TODO: Handling
        elif data_type == float:
            result = self._read_float(address, number_of_registers_for_value, holding_true_input_false)
            return result[0]
