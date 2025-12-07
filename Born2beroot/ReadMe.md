# 🖥️ Born2beRoot

[![42 Project](https://img.shields.io/badge/42-Born2beRoot-00babc?style=flat-square&logo=42)](https://github.com/yourusername/born2beroot)
![Grade](https://img.shields.io/badge/Grade-86%2F100-success?style=flat-square)
![OS](https://img.shields.io/badge/OS-Debian-red?style=flat-square)

## 📋 Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Security Setup](#security-setup)
- [Monitoring Script](#monitoring-script)

## 🎯 Description

**Born2beRoot** introduces you to the world of virtualization and system administration. You'll create your first virtual machine following strict rules.

## 🚀 Installation

### Virtual Machine Setup
- OS: Debian 12
- RAM: 1024 MB
- Disk: 30 GB VDI
- Encryption: LVM

## ⚙️ Configuration

### SSH Configuration
```bash
sudo apt install openssh-server
sudo nano /etc/ssh/sshd_config
# Port 4242
# PermitRootLogin no
sudo systemctl restart ssh
```

### UFW Firewall
```bash
sudo apt install ufw
sudo ufw allow 4242
sudo ufw enable
```

## 📊 Monitoring Script

```bash
#!/bin/bash
arch=$(uname -a)
pcpu=$(grep "physical id" /proc/cpuinfo | wc -l)
vcpu=$(grep "processor" /proc/cpuinfo | wc -l)
wall "Architecture: $arch
CPU physical: $pcpu
vCPU: $vcpu"
```

---
**Grade**: 86/100 | **Status**: Validated
