# tests/test_ip_utils.py

import unittest
from ip_fetcher.ip_utils import get_public_ip, get_private_ip

class TestIPUtils(unittest.TestCase):
    def test_get_public_ip(self):
        """Test the retrieval of the public IP address."""
        try:
            ip = get_public_ip()
            self.assertTrue(isinstance(ip, str) and ip.count('.') == 3)
        except RuntimeError as e:
            self.fail(f"get_public_ip raised RuntimeError: {e}")

    def test_get_private_ip(self):
        """Test the retrieval of the private IP address."""
        try:
            ip = get_private_ip()
            self.assertTrue(isinstance(ip, str) and ip.count('.') == 3)
        except RuntimeError as e:
            self.fail(f"get_private_ip raised RuntimeError: {e}")

if __name__ == "__main__":
    unittest.main()
