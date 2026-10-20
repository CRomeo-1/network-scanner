import argparse
import ipaddress
import platform
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
}


def ping(ip):
    # windows uses -n, linux/mac use -c
    flag = "-n" if platform.system() == "Windows" else "-c"
    result = subprocess.run(
        ["ping", flag, "1", "-w", "1000" if flag == "-n" else "1", str(ip)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def get_hostname(ip):
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except (socket.herror, socket.gaierror):
        return "-"


def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    is_open = s.connect_ex((str(ip), port)) == 0
    s.close()
    return is_open


def scan_host(ip):
    if not ping(ip):
        return None
    open_ports = [p for p in COMMON_PORTS if check_port(ip, p)]
    return {"ip": str(ip), "hostname": get_hostname(ip), "ports": open_ports}


def main():
    parser = argparse.ArgumentParser(description="Simple network scanner")
    parser.add_argument("network", help="network to scan, example: 192.168.1.0/24")
    parser.add_argument("-t", "--threads", type=int, default=50)
    args = parser.parse_args()

    network = ipaddress.ip_network(args.network, strict=False)
    hosts = list(network.hosts()) or [network.network_address]
    print(f"Scanning {network} ({len(hosts)} hosts)...\n")

    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        results = [r for r in pool.map(scan_host, hosts) if r]

    print(f"{'IP':<16}{'Hostname':<30}Open ports")
    print("-" * 70)
    for r in results:
        ports = ", ".join(f"{p}/{COMMON_PORTS[p]}" for p in r["ports"]) or "-"
        print(f"{r['ip']:<16}{r['hostname'][:28]:<30}{ports}")

    print(f"\n{len(results)} hosts up")


if __name__ == "__main__":
    main()
