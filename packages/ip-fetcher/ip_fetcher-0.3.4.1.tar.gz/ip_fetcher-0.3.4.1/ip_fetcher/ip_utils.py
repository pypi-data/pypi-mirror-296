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

def _check_version():
    try:
        current_version = pkg_resources.get_distribution("ip_fetcher").version
        response = requests.get("https://pypi.org/pypi/ip-fetcher/json")
        response.raise_for_status()
        latest_version = response.json()['info']['version']
        
        if current_version != latest_version:
            print(f"Warning: Your version of 'ip_fetcher' ({current_version}) is outdated.")
            print(f"The latest version available is {latest_version}.")
            print("To update to the latest version, run the following command:")
            print("pip install --upgrade ip_fetcher")

        else:
            print(f"'ip_fetcher' is up to date (version {current_version}).")
    except pkg_resources.DistributionNotFound:
        print("The 'ip_fetcher' package is not installed.")
    except requests.RequestException as e:
        print(f"Unable to fetch the latest version from PyPI: {e}")

_check_version()

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

def detect_proxy_or_vpn(ip_address):
    try:
        print(f"Checking if {ip_address} is a proxy or VPN...")
        response = requests.get(f"https://proxycheck.io/v2/{ip_address}")
        response.raise_for_status()
        data = response.json()
        
        if data[ip_address]["proxy"] == "yes":
            return f"{ip_address} is detected as a proxy or VPN."
        else:
            return f"{ip_address} is not detected as a proxy or VPN."
    except requests.RequestException as e:
        return f"Error checking proxy or VPN status: {e}"

def geolocation_lookup(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        response.raise_for_status()
        data = response.json()

        location_info = {
            "IP": data["ip"],
            "City": data.get("city", "N/A"),
            "Region": data.get("region", "N/A"),
            "Country": data.get("country", "N/A"),
            "Org": data.get("org", "N/A"),
            "Location": data.get("loc", "N/A")
        }
        
        return location_info
    except requests.RequestException as e:
        return f"Error fetching geolocation: {e}"

def store(ip_address, filename):
    """Store the IP address into a file."""
    try:
        with open(filename, "a") as file:
            file.write(ip_address + "\n")
        print(f"Stored IP address {ip_address} in {filename}.")
    except IOError as e:
        print(f"Error storing IP: {e}")

def read(filename):
    """Read all IP addresses from the file and return as a list."""
    try:
        with open(filename, "r") as file:
            ips = file.readlines()
        return [ip.strip() for ip in ips]  # Remove extra whitespaces
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
        return []

def read_specific(ip_address, filename):
    """Read specific IP address from the file and return if found."""
    try:
        with open(filename, "r") as file:
            ips = file.readlines()
        
        for ip in ips:
            if ip.strip() == ip_address:
                return ip_address  # Return the found IP address
        
        return None  # Return None if not found
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
        return None
