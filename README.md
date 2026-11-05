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
