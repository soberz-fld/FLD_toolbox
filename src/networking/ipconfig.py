import socket


def get_broadcast_of_devices_class_c_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # connect to any target website
    s.connect(('10.0.0.1', 0))
    ip_address = s.getsockname()[0]
    s.close()
    ip_blocks = str(ip_address).split('.')
    return ip_blocks[0] + '.' + ip_blocks[1] + '.' + ip_blocks[2] + '.' + str(255)


def get_ip_of_device() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # connect to any target website
    s.connect(('10.0.0.1', 0))
    ip_address = s.getsockname()[0]
    s.close()
    ip_blocks = str(ip_address).split('.')
    return ip_blocks[0] + '.' + ip_blocks[1] + '.' + ip_blocks[2] + '.' + ip_blocks[3]
