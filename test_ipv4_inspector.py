#!/usr/bin/env python3
"""Test script for ipv4_inspector module with validation"""

from ipv4_inspector import inspect_ipv4
import json

def validate_result(test_name, result, expected):
    """Validate test results against expected values"""
    print(f"\n{test_name}")
    print("=" * 60)
    print(json.dumps(result, indent=2))

    all_pass = True
    for key, expected_value in expected.items():
        if key not in result:
            print(f"❌ FAIL: Missing key '{key}'")
            all_pass = False
        elif result[key] != expected_value:
            print(f"❌ FAIL: {key} = {result[key]}, expected {expected_value}")
            all_pass = False

    if all_pass:
        print("✅ PASS: All validations passed")
    else:
        print("❌ FAIL: Some validations failed")

    return all_pass

# Track overall test results
tests_passed = 0
tests_failed = 0

# Test 1: Basic /24 network
result = inspect_ipv4("192.168.1.10/24")
expected = {
    "network_address": "192.168.1.0",
    "broadcast_address": "192.168.1.255",
    "prefix": 24,
    "netmask": "255.255.255.0",
    "host_range_begin": "192.168.1.1",
    "host_range_end": "192.168.1.254",
    "hosts": 256,
    "hostmask": "0.0.0.255",
    "network_increment": 1
}
if validate_result("Test 1: Basic /24 network", result, expected):
    tests_passed += 1
else:
    tests_failed += 1

# Test 2: /16 network with subnet calculation
result = inspect_ipv4("10.0.0.0/16", subnets_prefix=24)
expected = {
    "network_address": "10.0.0.0",
    "broadcast_address": "10.0.255.255",
    "prefix": 16,
    "netmask": "255.255.0.0",
    "host_range_begin": "10.0.0.1",
    "host_range_end": "10.0.255.254",
    "hosts": 65536,
    "hostmask": "0.0.255.255",
    "network_increment": 1,
    "subnets": {
        "subnets_prefix": 24,
        "subnets_count": 256,
        "subnets_hosts": 256
    }
}
if validate_result("Test 2: /16 with /24 subnets", result, expected):
    tests_passed += 1
else:
    tests_failed += 1

# Test 3: /31 network (point-to-point)
result = inspect_ipv4("192.168.100.0/31")
expected = {
    "network_address": "192.168.100.0",
    "broadcast_address": "192.168.100.1",
    "prefix": 31,
    "netmask": "255.255.255.254",
    "host_range_begin": "192.168.100.0",
    "host_range_end": "192.168.100.1",
    "hosts": 2,
    "hostmask": "0.0.0.1",
    "network_increment": 2
}
if validate_result("Test 3: /31 network (point-to-point)", result, expected):
    tests_passed += 1
else:
    tests_failed += 1

# Test 4: /32 network (host route)
result = inspect_ipv4("10.1.1.1/32")
expected = {
    "network_address": "10.1.1.1",
    "broadcast_address": "10.1.1.1",
    "prefix": 32,
    "netmask": "255.255.255.255",
    "host_range_begin": "10.1.1.1",
    "host_range_end": "10.1.1.1",
    "hosts": 1,
    "hostmask": "0.0.0.0",
    "network_increment": 1
}
if validate_result("Test 4: /32 network (host route)", result, expected):
    tests_passed += 1
else:
    tests_failed += 1

# Test 5: Large /8 network (performance test)
result = inspect_ipv4("10.0.0.0/8")
expected = {
    "network_address": "10.0.0.0",
    "broadcast_address": "10.255.255.255",
    "prefix": 8,
    "netmask": "255.0.0.0",
    "host_range_begin": "10.0.0.1",
    "host_range_end": "10.255.255.254",
    "hosts": 16777216,
    "hostmask": "0.255.255.255",
    "network_increment": 1
}
if validate_result("Test 5: Large /8 network (16M+ addresses)", result, expected):
    tests_passed += 1
else:
    tests_failed += 1

# Test 6: Whitespace format
result = inspect_ipv4("172.16.0.1 20")
expected = {
    "network_address": "172.16.0.0",
    "broadcast_address": "172.16.15.255",
    "prefix": 20,
    "netmask": "255.255.240.0",
    "host_range_begin": "172.16.0.1",
    "host_range_end": "172.16.15.254",
    "hosts": 4096,
    "hostmask": "0.0.15.255",
    "network_increment": 16
}
if validate_result("Test 6: Whitespace format '172.16.0.1 20'", result, expected):
    tests_passed += 1
else:
    tests_failed += 1

# Test 7: /28 network (verify network_increment calculation)
result = inspect_ipv4("192.168.1.0/28")
expected = {
    "network_address": "192.168.1.0",
    "broadcast_address": "192.168.1.15",
    "prefix": 28,
    "netmask": "255.255.255.240",
    "host_range_begin": "192.168.1.1",
    "host_range_end": "192.168.1.14",
    "hosts": 16,
    "hostmask": "0.0.0.15",
    "network_increment": 16
}
if validate_result("Test 7: /28 network (network_increment)", result, expected):
    tests_passed += 1
else:
    tests_failed += 1

# Test 8: /12 network (crossing octet boundaries)
result = inspect_ipv4("172.16.0.0/12")
expected = {
    "network_address": "172.16.0.0",
    "broadcast_address": "172.31.255.255",
    "prefix": 12,
    "netmask": "255.240.0.0",
    "host_range_begin": "172.16.0.1",
    "host_range_end": "172.31.255.254",
    "hosts": 1048576,
    "hostmask": "0.15.255.255",
    "network_increment": 16
}
if validate_result("Test 8: /12 network (octet boundary)", result, expected):
    tests_passed += 1
else:
    tests_failed += 1

# Test 9: Debug mode doesn't crash on /31
print("\nTest 9: Debug mode with /31 (should not crash)")
print("=" * 60)
debug = {"status": True, "level": 1}
result = inspect_ipv4("10.10.10.0/31", debug=debug)
expected = {
    "network_address": "10.10.10.0",
    "broadcast_address": "10.10.10.1",
    "prefix": 31,
    "host_range_begin": "10.10.10.0",
    "host_range_end": "10.10.10.1",
    "hosts": 2
}
# Check if key fields match (partial validation since debug prints output)
all_match = all(result[k] == v for k, v in expected.items())
if all_match:
    print("✅ PASS: Debug mode works correctly with /31")
    tests_passed += 1
else:
    print("❌ FAIL: Debug mode produced incorrect results")
    tests_failed += 1

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"✅ Passed: {tests_passed}")
print(f"❌ Failed: {tests_failed}")
print(f"Total: {tests_passed + tests_failed}")

if tests_failed == 0:
    print("\n🎉 All tests passed successfully!")
    exit(0)
else:
    print(f"\n⚠️  {tests_failed} test(s) failed")
    exit(1)
