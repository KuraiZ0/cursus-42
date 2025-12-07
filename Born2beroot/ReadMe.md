# 🐧 Born2BeRoot

![Status](https://img.shields.io/badge/Status-Completed-success) ![System](https://img.shields.io/badge/OS-Debian-red) ![Virtualization](https://img.shields.io/badge/VM-VirtualBox-orange)

## 📝 Description

**Born2BeRoot** est un projet d'introduction à la virtualisation et à l'administration système rigoureuse. L'objectif est de créer une machine virtuelle (VM) sécurisée tournant sous **Debian** (ou CentOS), sans interface graphique.

Ce projet impose le respect de règles strictes concernant le partitionnement, la gestion des utilisateurs, la sécurité réseau et le monitoring.

## ⚙️ Configuration Système

* **Hyperviseur :** VirtualBox
* **Système d'exploitation :** Debian (Stable)
* **Partitionnement :** LVM (Logical Volume Manager) chiffré.
* **Interface :** CLI uniquement (Command Line Interface).

## 🛡️ Sécurité & Services Mis en Place

### 1. Gestion des Utilisateurs et Mots de passe
* Politique de mots de passe forts configurée via `libpam-pwquality` (longueur min, complexité, expiration).
* Groupe `sudo` restreint et sécurisé.

### 2. Réseau et SSH
* Service SSH installé et configuré sur le **port 4242**.
* Connexion `root` via SSH désactivée.

### 3. Pare-feu (Firewall)
* Utilisation de **UFW** (Uncomplicated Firewall).
* Seul le port 4242 est ouvert vers l'extérieur.

### 4. Monitoring
* Développement d'un script `monitoring.sh` en Bash.
* Diffusion des informations système (CPU, RAM, Disque, Last boot, LVM status, Connexions actives) sur tous les terminaux toutes les 10 minutes via `cron`.

## 💻 Commandes Utiles

Se connecter à la VM depuis l'hôte :
<pre>
ssh <user>@<ip_address> -p 4242
Vérifier la configuration du pare-feu :
</pre>
<pre>
sudo ufw status
</pre>
Vérifier la politique de mots de passe :

<pre>
sudo chage -l <user>
</upre>

  Vérifier le partitionnement LVM :

<pre>
lsblk
</pre>
