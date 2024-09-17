from .ip_utils import (
    get_public_ip,
    get_private_ip,
    is_ipv4,
    is_ipv6,
    detect_proxy_or_vpn,
    store,  # Add this line to import the 'store' function
    read,   # If you are using the 'read' function, import it as well
    read_specific  # If you are using 'read_specific', import it too
)

import pkg_resources
import requests

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
        print("The 'ip_fetcher' package is not installed.")
    except requests.RequestException as e:
        print(f"Unable to fetch the latest version from PyPI: {e}")

# Automatically check the version when the package is imported
_check_version()
