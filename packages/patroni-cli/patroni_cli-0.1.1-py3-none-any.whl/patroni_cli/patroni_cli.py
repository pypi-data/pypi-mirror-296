import argparse
import requests
import sys
from requests.auth import HTTPBasicAuth

class PatroniCLI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
    
    def get_cluster_status(self):
        """Get the current cluster status and list all members."""
        url = f"{self.base_url}/cluster"
        try:
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            data = response.json()
            self.print_cluster_status(data)
        except requests.RequestException as e:
            print(f"Error fetching cluster status: {e}")
            sys.exit(1)

    def elect_new_leader(self, new_leader):
        """Elect a new leader by triggering a failover."""
        url = f"{self.base_url}/failover"
        current_leader = self.get_current_leader()
        if current_leader == new_leader:
            print(f"{new_leader} is already the leader. No failover required.")
            return
        
        payload = {
            "leader": current_leader,
            "candidate": new_leader
        }
        try:
            response = requests.post(url, json=payload, auth=self.auth)
            response.raise_for_status()
            print(f"Successfully triggered failover to {new_leader}.")
        except requests.RequestException as e:
            print(f"Error triggering failover: {e}")
            sys.exit(1)

    def switchover(self, target_leader=None):
        """Perform a switchover to the specified target leader or to a healthy node."""
        url = f"{self.base_url}/switchover"
        current_leader = self.get_current_leader()

        if target_leader:
            if current_leader == target_leader:
                print(f"{target_leader} is already the leader. No switchover required")
                return

            payload = {
                "leader": current_leader,
                "candidate": target_leader
            }
        else:
            # No target leader specified, switchover to any healthy node
            payload = {
                "leader": current_leader
                # No "candidate" field means Patroni will select any healthy node
            }

        try:
            response = requests.post(url, json=payload, auth=self.auth)
            response.raise_for_status()
            if target_leader:
                print(f"Successfully switched over to {target_leader}")
            else:
                print(f"Successfully switched over to a healthy node")
        except requests.RequestException as e:
            print(f"Error performing switchover: {e}")
            sys.exit(1)

    def get_current_leader(self):
        """Retrieve the current leader from the cluster."""
        url = f"{self.base_url}/cluster"
        try:
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            data = response.json()
            for member in data.get("members", []):
                if member.get("role") == "leader":
                    return member.get("name")
        except requests.RequestException as e:
            print(f"Error fetching current leader: {e}")
            sys.exit(1)
        return None

    def print_cluster_status(self, data):
        """Prints the current cluster status."""
        print("Cluster Status:")
        print("-" * 30)
        for member in data.get("members", []):
            print(f"Name: {member.get('name')}")
            print(f"Role: {member.get('role')}")
            print(f"State: {member.get('state')}")
            print(f"API URL: {member.get('api_url')}")
            print("-" * 30)


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool to manage Patroni vcluster, elect new leaders, and perform switchover."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Base URL of the Patroni API (e.g., http://localhost:8008)"
    )
    parser.add_argument(
        "--username",
        required=True,
        help="Username for HTTP Basic Authentication"
    )
    parser.add_argument(
        "--password",
        required=True,
        help="Password for HTTP Basic Authentication"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command to list cluster status
    subparsers.add_parser("status", help="Get the current cluster status")

    # Command to elect a new leader
    elect_parser = subparsers.add_parser("elect", help="Elect a new leader")
    elect_parser.add_argument(
        "new_leader", help="Name of the member to be elected as the new leader"
    )

    # Command to perform a switchover
    switchover_parser = subparsers.add_parser("switchover", help="Perform a switchover to a new leader or a healthy node")
    switchover_parser.add_argument(
        "target_leader", nargs='?', default=None, help="(Optional) Name of the member to be switched over as the new leader"
    )

    args = parser.parse_args()

    # Instantiate the PatroniCLI class with the base URL and authentication details
    patroni_cli = PatroniCLI(base_url=args.url, username=args.username, password=args.password)

    if args.command == "status":
        patroni_cli.get_cluster_status()
    elif args.command == "elect":
        patroni_cli.elect_new_leader(args.new_leader)
    elif args.command == "switchover":
        patroni_cli.switchover(args.target_leader)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
