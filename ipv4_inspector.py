import ipaddress
import re

def inspect_ipv4(ipAddress, subnets_prefix = 0, debug = {'status': False, 'level':0}):
    def hosts_in_subnet(cidr_prefix):
        """
        Calculate the number of hosts in a subnet given a CIDR prefix.

        Args:
        - cidr_prefix (int): CIDR prefix (e.g., 24 for a /24 subnet)

        Returns:
        - int: Number of hosts in the subnet
        """
        # Calculate total number of addresses in the subnet
        total_addresses = 2 ** (32 - cidr_prefix)

        return total_addresses

    def host_bits(x):
        if (x <= 8):
            return (8 - x)
        elif (x <= 16):
            return (16 - x)
        elif (x <= 24):
            return (24 - x)
        else:
            return (32 - x)

    def ip_increment(x):
        return pow(2,x)

    rc = re.compile(r"\s+") 
    rs = re.sub(rc, "/", ipAddress)
    data = ipaddress.ip_network(rs.strip() , strict=False)
    #     handles edge case prefixes length 0
    if (int(data.prefixlen) == 0):
            # print("Oops!  That was no valid number.  Try again...")
            return "Oops!  That was no valid number.  Try again..."
    results = {}
#     handles edge case prefixes lengths 31 and 32
    is_point_to_point = int(data.prefixlen) in [31, 32]

    results = {
        "network_address": str(data.network_address),
        "broadcast_address": str(data.broadcast_address),
        "prefix": data.prefixlen,
        "netmask": str(data.netmask),
        "host_range_begin": str(data.network_address) if is_point_to_point else str(data.network_address + 1),
        "host_range_end": str(data.broadcast_address) if is_point_to_point else str(data.broadcast_address - 1),
        "hosts": data.num_addresses,
        "hostmask": str(data.hostmask),
        "network_increment": ip_increment(host_bits(data.prefixlen))
    }
    

    if (subnets_prefix > 0):
        subnets = len(list(ipaddress.ip_network(rs).subnets(new_prefix=subnets_prefix)))
        results['subnets'] = {'subnets_prefix': subnets_prefix, 'subnets_count': subnets, 'subnets_hosts': hosts_in_subnet(subnets_prefix)}
    if (debug['status']):
        print("network_address: ", data.network_address)
        print("broadcast_address: ", data.broadcast_address)
        print("prefix: ", data.prefixlen)
        print("netmask: ", data.netmask)
        print("host_range: ", results['host_range_begin'], " - ", results['host_range_end'])
        print("hosts: ", data.num_addresses)
        print("hostmask: ", data.hostmask)
    return results