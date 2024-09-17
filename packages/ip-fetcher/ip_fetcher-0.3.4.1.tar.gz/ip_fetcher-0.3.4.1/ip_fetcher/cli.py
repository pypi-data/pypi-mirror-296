import argparse
from ip_fetcher.ip_utils import get_public_ip, get_private_ip

def main():
    parser = argparse.ArgumentParser(description="Fetch IP addresses")
    parser.add_argument(
        "--public",
        action="store_true",
        help="Fetch the public IP address"
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Fetch the private IP address"
    )

    args = parser.parse_args()

    if args.public:
        try:
            public_ip = get_public_ip()
            print(f"Public IP Address: {public_ip}")
        except Exception as e:
            print(f"Error fetching public IP address: {e}")

    if args.private:
        try:
            private_ip = get_private_ip()
            print(f"Private IP Address: {private_ip}")
        except Exception as e:
            print(f"Error fetching private IP address: {e}")

if __name__ == "__main__":
    main()
