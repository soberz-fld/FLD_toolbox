import pythonping


def ping_host_latency(host) -> (float, None):
    count = 16
    timeout = 4
    ping_result = pythonping.ping(target=host, count=count, timeout=timeout)

    if ping_result.rtt_min_ms == timeout*1000:  # Unreachable
        return None

    return ping_result.rtt_avg_ms
