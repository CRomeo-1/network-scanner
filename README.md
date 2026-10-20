# Network Scanner

A small Python tool I made to discover devices on a local network and check which common ports are open. I built it while studying for CCNA to understand ICMP, TCP connections and subnetting in practice.

## Features
- Finds live hosts with ping (ICMP)
- Looks up hostnames with reverse DNS
- Checks common ports (SSH, HTTP, HTTPS, RDP, ...) using TCP connect
- Uses threads so a /24 network is scanned fast
- Works on Windows, Linux and Mac
- No external libraries, only Python standard library

## Usage

```bash
python scanner.py 192.168.1.0/24
```

Options:
```
-t, --threads   number of threads (default 50)
```

Example output:
```
Scanning 192.168.1.0/24 (254 hosts)...

IP              Hostname                      Open ports
----------------------------------------------------------------------
192.168.1.1     router.home                   53/DNS, 80/HTTP, 443/HTTPS
192.168.1.15    desktop-pc                    445/SMB, 3389/RDP
192.168.1.20    -                             22/SSH

3 hosts up
```

## How it works
1. The CIDR range is split into host addresses using the `ipaddress` module
2. Each host gets one ping, if it replies it is marked as up
3. For live hosts, the tool tries a TCP connection to each port. If the 3-way handshake completes, the port is open
4. Hostnames come from a reverse DNS (PTR) lookup

## Note
Only scan networks you own or have permission to scan.
