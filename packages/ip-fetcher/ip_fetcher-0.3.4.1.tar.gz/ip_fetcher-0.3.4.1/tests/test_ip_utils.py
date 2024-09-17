import unittest
from ip_fetcher.ip_utils import get_public_ip, get_private_ip, is_ipv4, is_ipv6, check_ip_proxy_vpn, IPFetcherError

class TestIpUtils(unittest.TestCase):

    def test_get_public_ip(self):
        try:
            ip = get_public_ip()
            self.assertIsInstance(ip, str)
            self.assertNotEqual(ip, 'No IP found')
        except IPFetcherError as e:
            self.fail(f"get_public_ip() raised IPFetcherError: {e}")

    def test_get_private_ip(self):
        try:
            ip = get_private_ip()
            self.assertIsInstance(ip, str)
            self.assertNotEqual(ip, None)
        except IPFetcherError as e:
            self.fail(f"get_private_ip() raised IPFetcherError: {e}")

    def test_is_ipv4(self):
        self.assertTrue(is_ipv4("192.168.1.1"))
        self.assertFalse(is_ipv4("::1"))

    def test_is_ipv6(self):
        self.assertTrue(is_ipv6("::1"))
        self.assertFalse(is_ipv6("192.168.1.1"))

    def test_check_ip_proxy_vpn(self):
        try:
            result = check_ip_proxy_vpn("8.8.8.8")
            self.assertIsInstance(result, bool)
        except RuntimeError as e:
            self.fail(f"check_ip_proxy_vpn() raised RuntimeError: {e}")

if __name__ == '__main__':
    unittest.main()
