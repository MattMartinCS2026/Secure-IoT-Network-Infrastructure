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

- `nmap -sV -O -p- 192.168.20.10` — full port/service/OS scan of iot-device-1
- `nmap -sV -O -p- 192.168.20.11` — full port/service/OS scan of iot-device-2
- `nmap -sV -p- 192.168.10.1,192.168.20.1` — scan of iot-router's exposed services

**Expected result:** Only explicitly allowed ports/services are visible from
the admin/attacker network; all other ports should appear filtered/closed due
to the firewall ruleset.

**Result:** _TBD — fill in after running on live VM_

### 2. Brute-Force Testing

Used to test whether authentication on exposed services could be compromised
if reached from the attacker network.

- `hydra -l <username> -P /usr/share/wordlists/rockyou.txt.gz ssh://192.168.20.10`
- (Repeat against any other authenticated service found during scanning.)

**Expected result:** If SSH/authentication is not exposed to the admin
network per the firewall rules, this test should show no reachable login
surface. If reachable, it tests credential strength as a secondary control.

**Result:** _TBD — fill in after running on live VM_

### 3. DoS Simulation

Used to measure whether the firewall/router can detect and withstand a
traffic flood directed at the IoT devices.

- `hping3 -S --flood -p 80 192.168.20.10` — SYN flood against iot-device-1
- `hping3 --icmp --flood 192.168.20.10` — ICMP flood against iot-device-1

Firewall logs were monitored in real time during each test via:
`sudo journalctl -kf | grep DROP`

**Expected result:** The firewall should rate-limit or drop excess traffic
and log the activity, demonstrating resilience and visibility into the
attack rather than allowing it to pass through unchecked.

**Result:** _TBD — fill in after running on live VM_
