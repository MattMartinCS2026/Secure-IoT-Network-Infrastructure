# README

VirtualBox is used to simulate an IoT network with separate management/attacker and IoT networks. An Ubuntu Server router connects the two networks.


**Network Configuration:**

| Network | Subnet | VirtualBox Network Name |
|---|---|---|
| Admin/Attacker | 192.168.10.0/24 | `admin-net` |
| IoT | 192.168.20.0/24 | `iot-net` |

**Virtual Machines:**

| VM | IP Address | Purpose |
|---|---|---|
| `iot-router` | 192.168.10.1 / 192.168.20.1 | Routes traffic between networks |
| `iot-device-1` | 192.168.20.10 | Simulated IoT device |
| `iot-device-2` | 192.168.20.11 | Simulated IoT device |
| `iot-attacker` | 192.168.10.20 | Kali Linux VM used for network scanning, brute-force testing, and DoS simulations |

## Security Testing: Attacker VM

The `iot-attacker` VM (Kali Linux, 192.168.10.20) sits on the admin/attacker
network and is used to validate the effectiveness of the firewall and network
segmentation configured on `iot-router`. All testing is performed in the
isolated lab environment described above and is scoped to demonstrating
firewall behavior, detection, and resilience — not to cause disruption beyond
this controlled network.

### 1. Network Scanning

Used to confirm that only intended ports/services are reachable across the
network boundary.

`nmap -sV -O -p- <target>` run against iot-device-1, iot-device-2, and iot-router.

**Without security measures:** All three scans completed successfully, fully enumerating open ports, services, and OS details.
**With security measures:** All three scans failed to connect or never completed — firewall blocked reconnaissance traffic.

### 2. Brute-Force Testing

Used to test whether authentication on exposed services could be compromised
if reached from the attacker network.

`hydra -l <username> -P /usr/share/wordlists/rockyou.txt.gz ssh://192.168.20.10`

**Without security measures:** Attack reached the SSH service and ran to completion; no valid password found.
**With security measures:** Connection timed out — firewall blocked the attack before authentication could be attempted.

### 3. DoS Simulation

Used to measure whether the firewall/router can detect and withstand a
traffic flood directed at the IoT devices.

Firewall logs were monitored in real time during each test via:
`sudo journalctl -kf | grep DROP`

`hping3 -S --flood -p 80 192.168.20.10`

**Without security measures:** SYN flood reached iot-device-1, generating continuous SYN/RST traffic in the packet capture.
**With security measures:** No flood traffic reached iot-device-1 — `tcpdump` on the device showed zero incoming packets during the attack.
