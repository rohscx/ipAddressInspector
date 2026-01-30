---

# IPv4 Address Inspector

A lightweight Python utility for inspecting IPv4 networks and subnets.

This module parses IPv4 addresses and CIDR notation to return detailed network information, including address ranges, host counts, subnet details, and network increments.

It is built on Python’s standard `ipaddress` library with minimal external dependencies.

---

## Features

* **Parse** IPv4 addresses and CIDR notation
* **Calculate**:
* Network address
* Broadcast address
* Netmask and hostmask
* Host range
* Host count
* Network increment


* **Handle edge cases** (`/31`, `/32`)
* **Optional** subnet calculations
* **Optional** debug output
* **JSON-serializable** results

---

## Requirements

* Python 3.8+
* `netaddr` (optional, reserved for future extensions)

**Install dependencies:**

```bash
pip install netaddr

```

---

## Usage

### Import

```python
from ipv4_inspector import inspect_ipv4

```

### Basic Example

```python
result = inspect_ipv4("192.168.1.10/24")
print(result)

```

**Output:**

```json
{
    "network_address": "192.168.1.0",
    "broadcast_address": "192.168.1.255",
    "prefix": 24,
    "netmask": "255.255.255.0",
    "host_range_begin": "192.168.1.1",
    "host_range_end": "192.168.1.254",
    "hosts": 256,
    "hostmask": "0.0.0.255",
    "network_increment": 256
}

```

### With Subnet Calculation

```python
result = inspect_ipv4("10.0.0.0/16", subnets_prefix=24)

```

**Output includes subnet details:**

```json
"subnets": {
    "subnets_prefix": 24,
    "subnets_count": 256,
    "subnets_hosts": 256
}

```

### Debug Mode

Enable debug output to print network details to `stdout`:

```python
debug = {
    "status": True,
    "level": 1
}

inspect_ipv4("172.16.0.1/20", debug=debug)

```

---

## Function Reference

### `inspect_ipv4()`

`inspect_ipv4(ipAddress, subnets_prefix=0, debug={"status": False, "level": 0})`

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `ipAddress` | `str` | IPv4 address with CIDR (e.g. `192.168.1.1/24`) |
| `subnets_prefix` | `int` | New prefix length for subnetting (optional) |
| `debug` | `dict` | Debug configuration |

**Returns:** `dict` containing network metadata.

#### Returned Fields

| Field | Description |
| --- | --- |
| `network_address` | Network address |
| `broadcast_address` | Broadcast address |
| `prefix` | CIDR prefix length |
| `netmask` | Subnet mask |
| `host_range_begin` | First usable host |
| `host_range_end` | Last usable host |
| `hosts` | Total addresses in subnet |
| `hostmask` | Host mask |
| `network_increment` | Network increment size |
| `subnets` | Subnet info (if enabled) |

---

## Edge Case Handling

### `/31` and `/32` Networks

For point-to-point and host routes:

* `/31` and `/32` are handled without excluding network/broadcast addresses.
* Host range includes all available addresses.

### `/0` Networks

A prefix of `/0` is rejected and returns an error string.

---

## Design Notes

* Uses `ipaddress.ip_network(..., strict=False)` to allow host addresses.
* Avoids heavy dependencies (SciPy, Dask, Pandas).
* Designed for operational and network engineering workflows.
* Output is JSON-friendly.

**Example: Export to JSON**

```python
import json

result = inspect_ipv4("192.168.10.5/24")
print(json.dumps(result, indent=2))

```

---

## Limitations

* IPv4 only (no IPv6 support).
* Host count includes network and broadcast for `/0`–`/30`.
* `netaddr` is currently unused but reserved for future extensions.

---

## License

MIT License

---

## Roadmap

If you’d like, future enhancements may include:

* Packaging as a pip module
* CLI support (`ipv4-inspect 192.168.1.1/24`)
* Unit tests
* Optimized host counting for large subnets

---

Would you like me to generate a `setup.py` file or a `requirements.txt` to help you package this utility?s
