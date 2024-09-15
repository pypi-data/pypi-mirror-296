# ip_fetcher/ip_utils.py

import requests
import socket

def get_public_ip():
    """Fetches the public IP address of the user."""
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException as e:
        raise RuntimeError(f"Unable to fetch public IP address: {e}")

def get_private_ip():
    """Fetches the private IP address of the user."""
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except socket.error as e:
        raise RuntimeError(f"Unable to fetch private IP address: {e}")
