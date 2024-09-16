import requests
import socket
import ipaddress
import pkg_resources

class IPFetcherError(Exception):
    """Base class for exceptions in this module."""
    pass

class PublicIPError(IPFetcherError):
    """Raised when fetching the public IP fails."""
    pass

class PrivateIPError(IPFetcherError):
    """Raised when fetching the private IP fails."""
    pass

class InvalidIPError(IPFetcherError):
    """Raised when an invalid IP address is provided."""
    pass

def get_public_ip():
    """Fetches the public IP address of the user."""
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException as e:
        print(f"Primary API failed: {e}")
        try:
            response = requests.get("https://api.my-ip.io/ip.json")
            response.raise_for_status()
            return response.json().get("ip", "No IP found")
        except requests.RequestException as e:
            raise PublicIPError(f"Unable to fetch public IP address: {e}")

def get_private_ip():
    """Fetches the private IP address of the user."""
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except socket.error as e:
        raise PrivateIPError(f"Unable to fetch private IP address: {e}")

def is_ipv4(ip):
    """Checks if the given IP address is an IPv4 address."""
    try:
        return ipaddress.ip_address(ip).version == 4
    except ValueError:
        return False

def is_ipv6(ip):
    """Checks if the given IP address is an IPv6 address."""
    try:
        return ipaddress.ip_address(ip).version == 6
    except ValueError:
        return False

def check_ip_proxy_vpn(ip):
    """Checks if the given IP address is a known proxy or VPN."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        response.raise_for_status()
        data = response.json()
        org = data.get('org', '').lower()
        return 'proxy' in org or 'vpn' in org
    except requests.RequestException as e:
        raise RuntimeError(f"Unable to check IP for proxy or VPN: {e}")

def _check_version():
    """Checks if the ip_fetcher library is up to date."""
    try:
        current_version = pkg_resources.get_distribution("ip_fetcher").version
        response = requests.get("https://pypi.org/pypi/ip-fetcher/json")
        response.raise_for_status()
        latest_version = response.json()['info']['version']
        if current_version != latest_version:
            print(f"Warning: Your version of the 'ip_fetcher' library ({current_version}) is outdated.")
            print(f"The latest version available is {latest_version}.")
            print("To update to the latest version, run the following command:")
            print("pip install --upgrade ip_fetcher")
    except pkg_resources.DistributionNotFound:
        # Handle the case where the package is not installed
        pass
    except requests.RequestException as e:
        print(f"Unable to fetch the latest version from PyPI: {e}")

# Automatically check the version when the package is imported
_check_version()
