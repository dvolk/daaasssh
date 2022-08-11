"""Make a DAaaS hosts and ssh config file."""

import json
import logging
import pathlib
import subprocess
import sys
import re
import os

import argh
import requests

logging.basicConfig(level=logging.INFO)


def get_ip(hostname):
    """Run host to get ip."""
    return subprocess.check_output(["host", hostname]).decode().split()[3]


def make_unique_name(name, names):
    """Create a name that's not in names, appending numbers if necessary."""
    if name not in names:
        return name
    i = 1
    while True:
        name_new = f"{name}_{i}"
        if name_new not in names:
            return name_new
        i = i + 1


def platform():
    """Open json file and write out platform_hosts.txt and platform_ssh_config.txt."""
    infile = "platform.json"
    if not pathlib.Path(infile).exists():
        logging.fatal(f"Couldn't find {infile}.\n\nPlease see README.md\n")
        sys.exit(1)

    with open(infile) as f:
        platform = json.load(f)

    hosts_out = open("platform_hosts.txt", "w")
    ssh_config_out = open("platform_ssh_config.txt", "w")

    names = list()

    for host in platform["_items"]:
        env = host["environment"].lower()
        readable_name = host["readable_name"].lower().replace(" ", "_")
        ip = get_ip(host["hostname"])
        nice_name = f"{env}_{readable_name}"
        nice_name = make_unique_name(nice_name, names)
        names.append(nice_name)
        hosts_out.write(f"{nice_name} {ip}\n")
        ssh_config_out.write(f"Host pl_{nice_name}\n")
        ssh_config_out.write(f"    HostName {ip}\n")
        ssh_config_out.write("    User root\n")
        ssh_config_out.write("    StrictHostKeyChecking no\n")
        ssh_config_out.write("    LogLevel QUIET\n")
        ssh_config_out.write("    UserKnownHostsFile /dev/null\n\n")


def workspaces(infile):
    """Open json file and write out workspaces_hosts.txt and workspaces_ssh_config.txt."""
    if not pathlib.Path(infile).exists():
        logging.fatal(f"Couldn't find {infile}.\n\nPlease see README.md\n")
        sys.exit(1)

    with open(infile) as f:
        platform = json.load(f)

    hosts_out = open(f"{infile}_hosts.txt", "w")
    ssh_config_out = open(f"{infile}_ssh_config.txt", "w")

    names = list()

    for host in platform["_items"]:
        if host["state"] != "CLAIMED":
            continue
        tag = host["tag"].lower()
        user = host["parameters"]["users"][0]["platformname"]
        readable_name = re.sub("[^0-9a-zA-Z]+", "_", host["name"].lower())
        ip = get_ip(host["hostname"])
        nice_name = f"{user}_{tag}_{readable_name}"
        nice_name = make_unique_name(nice_name, names)
        names.append(nice_name)
        hosts_out.write(f"{nice_name} {ip}\n")
        ssh_config_out.write(f"Host wk_{nice_name}\n")
        ssh_config_out.write(f"    HostName {ip}\n")
        ssh_config_out.write("    User root\n")
        ssh_config_out.write("    StrictHostKeyChecking no\n")
        ssh_config_out.write("    LogLevel QUIET\n")
        ssh_config_out.write("    UserKnownHostsFile /dev/null\n\n")


def deploy_ssh():
    """Move hosts to ssh config."""
    os.system("cat platform_ssh_config.txt > ~/.ssh/config")
    os.system("cat workspaces*_ssh_config.txt >> ~/.ssh/config")


def get_data():
    """Get platform and workspace data."""
    p = requests.get(
        "https://host-172-16-112-161.nubes.stfc.ac.uk/hosts/",
        auth=requests.auth.HTTPBasicAuth(
            os.environ.get("P_USERNAME"), os.environ.get("P_PASSWORD")
        ),
    ).json()
    w_dev = requests.get(
        'https://host-172-16-100-166.nubes.stfc.ac.uk/workspaces?max_results=500&where={"state":"CLAIMED"}',
        auth=requests.auth.HTTPBasicAuth(
            os.environ.get("W_DEV_USERNAME"), os.environ.get("W_DEV_PASSWORD")
        ),
    ).json()
    w_prod = requests.get(
        'https://host-172-16-105-103.nubes.stfc.ac.uk/workspaces?max_results=500&where={"state":"CLAIMED"}',
        auth=requests.auth.HTTPBasicAuth(
            os.environ.get("W_PROD_USERNAME"), os.environ.get("W_PROD_PASSWORD")
        ),
    ).json()
    with open("platform.json", "w") as f:
        f.write(json.dumps(p, indent=4))
    with open("workspaces-dev.json", "w") as f:
        f.write(json.dumps(w_dev, indent=4))
    with open("workspaces-prod.json", "w") as f:
        f.write(json.dumps(w_prod, indent=4))


def go():
    """Get data and write to config."""
    logging.info("Getting data from registers")
    get_data()
    logging.info("OK")

    logging.info("Parsing platform json")
    platform()
    logging.info("OK")

    logging.info("Parsing workspaces dev json")
    workspaces("workspaces-dev.json")
    logging.info("OK")

    logging.info("Parsing workspaces prod json")
    workspaces("workspaces-prod.json")
    logging.info("OK")

    logging.info("Writing SSH config")
    deploy_ssh()
    logging.info("OK")


if __name__ == "__main__":
    argh.dispatch_commands([platform, workspaces, deploy_ssh, get_data, go])
