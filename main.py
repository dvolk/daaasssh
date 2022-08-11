import json
import subprocess


def get_ip(hostname):
    return subprocess.check_output(["host", hostname]).decode().split()[3]


def main():
    with open("platform.json") as f:
        platform = json.load(f)

    hosts_out = open("hosts.txt", "w")
    ssh_config_out = open("ssh_config.txt", "w")

    for host in platform["_items"]:
        hostname = host["hostname"].lower()
        env = host["environment"].lower()
        readable_name = host["readable_name"].lower().replace(" ", "_")
        ip = get_ip(host["hostname"])
        host_entry = f"{env}_{readable_name} {ip}"
        hosts_out.write(host_entry + "\n")
        ssh_config_out.write(f"Host ssh_{host_entry}\n")
        ssh_config_out.write(f"    HostName {ip}")
        ssh_config_out.write(f"    User root")


if __name__ == "__main__":
    main()